import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import warnings
import time

warnings.filterwarnings('ignore')

# ==========================================
# CONFIGURATION
# ==========================================
url = "http://localhost:8086"
token = "W3cPRGkq7ds7JHFNtuciiVqEVPGugFye82mykiLWWee2FMxLDflsqsHk8OJaavTS9Sjh1_H31xU4yh3J5IC9RA=="
org = "unibs"
bucket = "crime_data"

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# ==========================================
# 1. DATA LOADING & PREPROCESSING
# ==========================================
print("--- 1. Data Loading & Preprocessing ---")

# Caricamento Dataset
csv_path = "Crime_Data_from_2020_to_Present.csv"
df = pd.read_csv(csv_path)

# --- Data Cleaning ---
# Conversione date
df['Date Rptd'] = pd.to_datetime(df['Date Rptd'], format='%m/%d/%Y %I:%M:%S %p')
df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], format='%m/%d/%Y %I:%M:%S %p')

# Filtro dati validi
# 1. Coordinate non nulle
df = df[(df['LAT'] != 0) & (df['LON'] != 0)]

# 2. Date non future (oltre Nov 2025)
cutoff_date = pd.Timestamp('2025-11-30')
df = df[df['DATE OCC'] <= cutoff_date]

# 3. Tipi di crimine validi
df = df.dropna(subset=['Crm Cd'])

print(f"Record validi dopo il filtro: {len(df)}")

# --- Feature Engineering ---
def get_season(date):
    month = date.month
    if month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Autumn"
    else:
        return "Winter"

def get_day_night(time_occ):
    hour = int(time_occ / 100)
    if 6 <= hour < 18:
        return "Day"
    else:
        return "Night"

df['Season'] = df['DATE OCC'].apply(get_season)
df['DayNight'] = df['TIME OCC'].apply(get_day_night)
df['WeaponFlag'] = df['Weapon Used Cd'].notna()
df['Part 1-2'] = df['Part 1-2'].astype(str)
df['DR_NO'] = df['DR_NO'].astype(str) # Importante per uso come tag

# --- Alert Logic Setup ---
print("\n--- Alert Logic Setup ---")
# Raggruppiamo per data per calcolare le soglie storiche
daily_stats = df.groupby(df['DATE OCC'].dt.date).agg(
    Total_Crimes=('DR_NO', 'count'),
    Violent_Crimes=('Part 1-2', lambda x: (x=='1').sum()),
    Weapon_Pct=('WeaponFlag', 'mean')
)

# Calcolo massimi storici
max_daily_crimes = daily_stats['Total_Crimes'].max()
max_daily_violent = daily_stats['Violent_Crimes'].max()
max_daily_weapon_pct = daily_stats['Weapon_Pct'].max()

# Soglie: Warning > 5% del max, Alarm > 10% del max
THRESHOLDS = {
    'Total_Crimes': {
        'Warning': max_daily_crimes * 1.05,
        'Alarm': max_daily_crimes * 1.10
    },
    'Violent_Crimes': {
        'Warning': max_daily_violent * 1.05,
        'Alarm': max_daily_violent * 1.10
    },
    'Weapon_Pct': {
        'Warning': max_daily_weapon_pct * 1.05,
        'Alarm': max_daily_weapon_pct * 1.10
    }
}

for metric, values in THRESHOLDS.items():
    print(f"{metric}: Max={daily_stats[metric].max():.2f}, Warning={values['Warning']:.2f}, Alarm={values['Alarm']:.2f}")

def check_alert(date, metrics):
    alerts = []
    for key, val in metrics.items():
        if key in THRESHOLDS:
            if val > THRESHOLDS[key]['Alarm']:
                alerts.append(f"🚨 [ALARM] {date} - {key}: {val:.2f} > {THRESHOLDS[key]['Alarm']:.2f}")
            elif val > THRESHOLDS[key]['Warning']:
                alerts.append(f"⚠️ [WARNING] {date} - {key}: {val:.2f} > {THRESHOLDS[key]['Warning']:.2f}")
    
    if alerts:
        for alert in alerts:
            print(alert)

# ==========================================
# 2. INFLUXDB WRITING
# ==========================================
print("\n--- 2. InfluxDB Writing ---")

write_options = WriteOptions(
    batch_size=5000,
    flush_interval=1000,
    jitter_interval=0,
    retry_interval=5000,
    max_retries=5,
    max_retry_delay=30000,
    exponential_base=2
)

write_api = client.write_api(write_options=write_options)

df_influx = df.copy()
df_influx = df_influx.set_index('DATE OCC')

df_influx = df_influx.rename(columns={
    'AREA NAME': 'Area_Name',
    'Part 1-2': 'Part_1_2',
    'Crm Cd Desc': 'Crm_Cd_Desc',
    'Status Desc': 'Status_Desc',
    'LAT': 'Lat',
    'LON': 'Lon',
    'Vict Age': 'Vict_Age',
    'Crm Cd': 'Crm_Cd',
    'Rpt Dist No': 'Rpt_Dist_No',
    'DR_NO': 'DR_NO'
})

# DR_NO aggiunto ai tags per garantire unicità
tags = ['Area_Name', 'Part_1_2', 'Season', 'DayNight', 'WeaponFlag', 'Crm_Cd_Desc', 'Status_Desc', 'DR_NO']
fields = ['Lat', 'Lon', 'Vict_Age', 'Crm_Cd', 'Rpt_Dist_No']

print("Inizio scrittura su InfluxDB (questo potrebbe richiedere tempo)...")
start_time = time.time()

try:
    # Scrittura in batch
    write_api.write(bucket=bucket, org=org, record=df_influx, data_frame_measurement_name='crimes', data_frame_tag_columns=tags)
    print("Scrittura completata.")
except Exception as e:
    print(f"Errore durante la scrittura: {e}")

write_api.close()
print(f"Tempo impiegato: {time.time() - start_time:.2f} secondi")

# Simulazione Alert
print("\n--- Simulazione Alert (Ultimi 5 giorni) ---")
for date, row in daily_stats.tail(5).iterrows():
    metrics = {
        'Total_Crimes': row['Total_Crimes'],
        'Violent_Crimes': row['Violent_Crimes'],
        'Weapon_Pct': row['Weapon_Pct']
    }
    check_alert(date, metrics)

# ==========================================
# 3. ANALYTICAL QUERIES
# ==========================================
print("\n--- 3. Analytical Queries ---")

# Q1: Media crimini giornalieri per Area e Stagione
print("Q1: Media crimini giornalieri per Area e Stagione...")
q1 = f'''
from(bucket: "{bucket}")
  |> range(start: 2020-01-01T00:00:00Z, stop: 2025-12-31T23:59:59Z)
  |> filter(fn: (r) => r["_measurement"] == "crimes")
  |> filter(fn: (r) => r["_field"] == "Lat") 
  |> group(columns: ["Area_Name", "Season"])
  |> count()
'''
# Nota: Usiamo Lat come campo proxy per contare i record.
# Il count() restituisce il totale per il periodo.
# Per ottenere la media giornaliera, dividiamo per il numero stimato di giorni per stagione in 5 anni.
# 5 anni * 90 giorni/stagione = 450 giorni.
result_q1 = query_api.query_data_frame(q1)
if not result_q1.empty:
    result_q1['daily_avg'] = result_q1['_value'] / 450 
    pivot_q1 = result_q1.pivot(index='Area_Name', columns='Season', values='daily_avg')
    pivot_q1.plot(kind='bar', figsize=(15, 8), width=0.8)
    plt.title('Q1: Media Giornaliera Crimini per Area e Stagione')
    plt.ylabel('Media Giornaliera')
    plt.tight_layout()
    plt.show()

# Q2: Distribuzione Part 1/2 per fasce orarie (Luglio 2023)
print("\nQ2: Distribuzione Part 1/2 Day/Night (Luglio 2023)...")
q2 = f'''
from(bucket: "{bucket}")
  |> range(start: 2023-07-01T00:00:00Z, stop: 2023-07-31T23:59:59Z)
  |> filter(fn: (r) => r["_measurement"] == "crimes")
  |> filter(fn: (r) => r["_field"] == "Lat")
  |> group(columns: ["Part_1_2", "DayNight"])
  |> count()
'''
result_q2 = query_api.query_data_frame(q2)
if not result_q2.empty:
    pivot_q2 = result_q2.pivot(index='DayNight', columns='Part_1_2', values='_value')
    pivot_q2.plot(kind='bar', figsize=(10, 6))
    plt.title('Q2: Crimini Part 1 vs Part 2 (Luglio 2023)')
    plt.ylabel('Conteggio')
    plt.show()

# Q3: Giornata con maggior numero di crimini violenti per Area
print("\nQ3: Giornata con max crimini violenti per Area...")
q3 = f'''
from(bucket: "{bucket}")
  |> range(start: 2020-01-01T00:00:00Z, stop: 2025-12-31T23:59:59Z)
  |> filter(fn: (r) => r["_measurement"] == "crimes")
  |> filter(fn: (r) => r["Part_1_2"] == "1")
  |> filter(fn: (r) => r["_field"] == "Lat")
  |> group(columns: ["Area_Name"])
  |> window(every: 1d)
  |> count()
  |> duplicate(column: "_start", as: "_time")
  |> window(every: inf)
  |> max()
'''
try:
    result_q3 = query_api.query_data_frame(q3)
    if not result_q3.empty:
        print(result_q3[['Area_Name', '_time', '_value']].sort_values('_value', ascending=False).head(10))
    else:
        print("Nessun dato per Q3")
except Exception as e:
    print(f"Errore Q3: {e}")

# Q4: Età media vittime per Categoria e Anno
print("\nQ4: Età media vittime...")
q4 = f'''
from(bucket: "{bucket}")
  |> range(start: 2020-01-01T00:00:00Z, stop: 2025-12-31T23:59:59Z)
  |> filter(fn: (r) => r["_measurement"] == "crimes")
  |> filter(fn: (r) => r["_field"] == "Vict_Age")
  |> filter(fn: (r) => r["_value"] > 0)
  |> group(columns: ["Part_1_2"])
  |> window(every: 1y)
  |> mean()
  |> duplicate(column: "_start", as: "Year")
  |> window(every: inf)
'''
result_q4 = query_api.query_data_frame(q4)
if not result_q4.empty:
    result_q4['Year'] = pd.to_datetime(result_q4['Year']).dt.year
    print(result_q4[['Part_1_2', 'Year', '_value']])

# ==========================================
# 4. CLUSTERING INCREMENTALE
# ==========================================
print("\n--- 4. Clustering Incrementale ---")
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler

# Aggreghiamo i dati usando Pandas
df['Year'] = df['DATE OCC'].dt.year
agg_df = df.groupby(['Area_Name', 'Season', 'Year']).agg(
    Total_Crimes=('DR_NO', 'count'),
    Weapon_Pct=('WeaponFlag', 'mean'),
    Night_Pct=('DayNight', lambda x: (x=='Night').mean()),
    Violent_Pct=('Part 1-2', lambda x: (x=='1').mean())
).reset_index()

features = ['Total_Crimes', 'Weapon_Pct', 'Night_Pct', 'Violent_Pct']
X = agg_df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train su 2020-2024
train_mask = agg_df['Year'] < 2025
X_train = X_scaled[train_mask]
X_test = X_scaled[~train_mask]

kmeans = MiniBatchKMeans(n_clusters=4, random_state=42, batch_size=256)
kmeans.fit(X_train)

agg_df.loc[train_mask, 'Cluster'] = kmeans.labels_

if len(X_test) > 0:
    agg_df.loc[~train_mask, 'Cluster'] = kmeans.predict(X_test)

print("\n--- Centroidi dei Cluster ---")
centroids = scaler.inverse_transform(kmeans.cluster_centers_)
centroid_df = pd.DataFrame(centroids, columns=features)
print(centroid_df)

print("\n--- Confronto Distribuzione Cluster 2020 vs 2025 ---")
cluster_dist = agg_df.groupby(['Year', 'Cluster']).size().unstack(fill_value=0)
print(cluster_dist.loc[[2020, 2025]] if 2025 in cluster_dist.index else cluster_dist)

cluster_dist.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Evoluzione dei Cluster nel Tempo')
plt.ylabel('Numero di Aree/Stagioni')
plt.show()
