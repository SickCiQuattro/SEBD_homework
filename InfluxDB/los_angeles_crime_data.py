import pandas as pd
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions

# ==========================================
# 1. CONFIGURAZIONE
# ==========================================
url = "http://localhost:8086"
token = "W3cPRGkq7ds7JHFNtuciiVqEVPGugFye82mykiLWWee2FMxLDflsqsHk8OJaavTS9Sjh1_H31xU4yh3J5IC9RA=="
org = "unibs"
bucket = "crime_data"

# Aumentiamo il timeout per evitare errori nelle aggregazioni future
client = InfluxDBClient(url=url, token=token, org=org, timeout=60_000)

write_api = client.write_api(
    write_options=WriteOptions(
        batch_size=2000,       
        flush_interval=5000, 
        jitter_interval=1000, 
        retry_interval=5000
    )
)

# ==========================================
# 2. CARICAMENTO E PRE-CALCOLO SOGLIE
# ==========================================
print("📂 Caricamento Dataset in Pandas...")
csv_path = "Crime_Data_from_2020_to_Present.csv"
df = pd.read_csv(csv_path)

# Conversione Date e Ordinamento (Fondamentale per la simulazione cronologica)
df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['Date Rptd'] = pd.to_datetime(df['Date Rptd'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df = df.sort_values(by='DATE OCC') # Ordiniamo per data per simulare il flusso temporale

# --- CALCOLO DEI MASSIMI STORICI (BASELINE) ---
print("📊 Analisi preliminare per definire le soglie di allarme...")

# Raggruppiamo per giorno per calcolare le metriche giornaliere
daily_stats = df.groupby(df['DATE OCC'].dt.date).agg(
    total_crimes=('DR_NO', 'count'),
    violent_crimes=('Part 1-2', lambda x: (x == 1).sum()), # Part 1 = Crimini gravi/violenti
    weapon_crimes=('Weapon Used Cd', lambda x: x.notna().sum()) # Se c'è un codice, c'è un'arma
)

# Calcoliamo la percentuale giornaliera di armi
daily_stats['weapon_pct'] = (daily_stats['weapon_crimes'] / daily_stats['total_crimes']) * 100

# Troviamo i valori massimi "normali" (Baseline)
max_daily_total = daily_stats['total_crimes'].max()
max_daily_violent = daily_stats['violent_crimes'].max()
# Per la % armi, usiamo il max, ma filtriamo giorni con pochissimi crimini per evitare outlier statistici (es. 1 crimine, 1 arma = 100%)
max_daily_weapon_pct = daily_stats[daily_stats['total_crimes'] > 10]['weapon_pct'].max()

# --- IMPOSTAZIONE REGOLE (5% e 10%) ---
# Warning: Superamento del 5% rispetto al massimo storico
# Alarm: Superamento del 10% rispetto al massimo storico

limits = {
    'total': {
        'warn': max_daily_total * 1.05, 
        'alarm': max_daily_total * 1.10
    },
    'violent': {
        'warn': max_daily_violent * 1.05, 
        'alarm': max_daily_violent * 1.10
    },
    'weapon_pct': {
        'warn': max_daily_weapon_pct * 1.05, 
        'alarm': max_daily_weapon_pct * 1.10
    }
}

print(f"   [TOTALE] Max Storico: {max_daily_total} -> Warn: {limits['total']['warn']:.1f}, Alarm: {limits['total']['alarm']:.1f}")
print(f"   [VIOLENTI] Max Storico: {max_daily_violent} -> Warn: {limits['violent']['warn']:.1f}, Alarm: {limits['violent']['alarm']:.1f}")
print(f"   [ARMA %] Max Storico: {max_daily_weapon_pct:.1f}% -> Warn: {limits['weapon_pct']['warn']:.1f}%, Alarm: {limits['weapon_pct']['alarm']:.1f}%")
print("-" * 50)

# ==========================================
# 3. FUNZIONI DI SUPPORTO
# ==========================================

def get_season(date):
    """Restituisce la stagione basata sulla data"""
    m, d = date.month, date.day
    if (m == 12 and d >= 21) or m in [1, 2] or (m == 3 and d < 21): return "Winter"
    elif (m == 3 and d >= 21) or m in [4, 5] or (m == 6 and d < 21): return "Spring"
    elif (m == 6 and d >= 21) or m in [7, 8] or (m == 9 and d < 21): return "Summer"
    else: return "Autumn"

def get_day_night(time_occ):
    if pd.isna(time_occ): return "Unknown"
    h = int(time_occ / 100)
    return "Day" if 6 <= h <= 18 else "Night"

def check_and_print_alerts(date, stats, limits):
    """Verifica le soglie e stampa a video"""
    alerts = []
    
    # 1. Controllo Totale Giornaliero
    if stats['total'] > limits['total']['alarm']:
        alerts.append(f"🔴 ALARM Totale: {stats['total']} (Soglia {limits['total']['alarm']:.0f})")
    elif stats['total'] > limits['total']['warn']:
        alerts.append(f"⚠️ WARNING Totale: {stats['total']} (Soglia {limits['total']['warn']:.0f})")

    # 2. Controllo Crimini Violenti
    if stats['violent'] > limits['violent']['alarm']:
        alerts.append(f"🔴 ALARM Violenti: {stats['violent']} (Soglia {limits['violent']['alarm']:.0f})")
    elif stats['violent'] > limits['violent']['warn']:
        alerts.append(f"⚠️ WARNING Violenti: {stats['violent']} (Soglia {limits['violent']['warn']:.0f})")

    # 3. Controllo % Armi
    pct = (stats['weapon'] / stats['total'] * 100) if stats['total'] > 0 else 0
    if pct > limits['weapon_pct']['alarm']:
        alerts.append(f"🔴 ALARM Armi %: {pct:.1f}% (Soglia {limits['weapon_pct']['alarm']:.1f}%)")
    elif pct > limits['weapon_pct']['warn']:
        alerts.append(f"⚠️ WARNING Armi %: {pct:.1f}% (Soglia {limits['weapon_pct']['warn']:.1f}%)")

    if alerts:
        print(f"📅 {date}: " + " | ".join(alerts))

# ==========================================
# 4. LOOP DI CARICAMENTO SIMULATO
# ==========================================

print("🚀 Inizio simulazione caricamento dati...")
start_time = time.time()

cnt_written = 0
cnt_excluded = 0

# Variabili per accumulo giornaliero
current_date = None
daily_accumulator = {'total': 0, 'violent': 0, 'weapon': 0}
cutoff_date = pd.Timestamp('2025-11-30')

for idx, row in df.iterrows():
    
    # --- FILTRI (Esclusioni) ---
    if (row['LAT'] == 0 and row['LON'] == 0) or \
       (pd.isna(row['DATE OCC']) or row['DATE OCC'] > cutoff_date) or \
       (pd.isna(row['Crm Cd'])):
        cnt_excluded += 1
        continue

    # --- SIMULAZIONE TEMPORALE & ALERT ---
    row_date = row['DATE OCC'].date()

    # Cambio giorno: analizziamo i dati del giorno appena concluso
    if row_date != current_date:
        if current_date is not None:
            check_and_print_alerts(current_date, daily_accumulator, limits)
        
        # Reset per il nuovo giorno
        current_date = row_date
        daily_accumulator = {'total': 0, 'violent': 0, 'weapon': 0}

    # --- AGGIORNAMENTO CONTATORI GIORNALIERI ---
    daily_accumulator['total'] += 1
    
    # Part 1 = Crimini gravi (Violenti)
    if row['Part 1-2'] == 1:
        daily_accumulator['violent'] += 1
    
    # Arma presente
    has_weapon = pd.notna(row['Weapon Used Cd'])
    if has_weapon:
        daily_accumulator['weapon'] += 1

    # --- CREAZIONE POINT INFLUXDB ---
    unique_ts = row['DATE OCC'] + pd.Timedelta(microseconds=idx % 1_000_000)
    
    # Preparazione dati puliti
    season = get_season(row['DATE OCC'])
    day_night = get_day_night(row['TIME OCC'])
    weapon_flag = "True" if has_weapon else "False"
    sex = str(row['Vict Sex']) if pd.notna(row['Vict Sex']) and row['Vict Sex'] in ['M','F'] else "X"
    
    point = Point("crime_report") \
        .tag("area_name", str(row['AREA NAME'])) \
        .tag("area_id", str(int(row['AREA']))) \
        .tag("district", str(int(row['Rpt Dist No']))) \
        .tag("part_category", str(int(row['Part 1-2']))) \
        .tag("weapon_present", weapon_flag) \
        .tag("season", season) \
        .tag("time_period", day_night) \
        .field("n_crimini", 1) \
        .field("dr_no", int(row['DR_NO'])) \
        .field("lat", float(row['LAT'])) \
        .field("lon", float(row['LON'])) \
        .field("crime_cd", int(row['Crm Cd'])) \
        .field("vict_age", int(row['Vict Age']) if pd.notna(row['Vict Age']) and row['Vict Age'] > 0 else 0) \
        .field("vict_sex", sex) \
        .time(unique_ts, WritePrecision.US)

    write_api.write(bucket=bucket, org=org, record=point)
    cnt_written += 1

    if cnt_written % 100000 == 0:
        print(f"   ...elaborati {cnt_written} crimini...")

# Controllo dell'ultimo giorno rimasto nel buffer fuori dal loop
if current_date is not None:
    check_and_print_alerts(current_date, daily_accumulator, limits)

write_api.close() # Flush finale e chiusura

print(f"\n✅ CARICAMENTO COMPLETATO.")
print(f"   - Record scritti: {cnt_written}")
print(f"   - Record scartati: {cnt_excluded}")
print(f"   - Tempo: {time.time() - start_time:.2f} sec")







import pandas as pd
import time
from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import WriteOptions

# --- 1. PREPARAZIONE DATI VETTORIALE (Molto più veloce) ---
# Rinominiamo le colonne per facilitare l'accesso con itertuples (niente spazi)
df.rename(columns={
    'DATE OCC': 'DATE_OCC', 
    'Crm Cd': 'Crm_Cd',
    'Weapon Used Cd': 'Weapon_Used_Cd',
    'Part 1-2': 'Part_1_2',
    'AREA NAME': 'AREA_NAME',
    'Rpt Dist No': 'Rpt_Dist_No',
    'TIME OCC': 'TIME_OCC'
}, inplace=True)

# Creiamo flag booleane PRIMA del ciclo (vettorizzazione)
# True = 1, False = 0. Questo ci permette di sommare direttamente nel ciclo.
df['is_weapon'] = df['Weapon_Used_Cd'].notna()
# Convertiamo in numerico forzato e controlliamo se è 1
df['is_violent'] = pd.to_numeric(df['Part_1_2'], errors='coerce').fillna(0) == 1

# Ordiniamo per data (fondamentale per la logica sequenziale)
df = df.sort_values(by='DATE_OCC')

# --- Funzione Helper Alert ---
def check_daily_alerts(day, total, violent, weapon_count, thresholds):
    """Controlla e stampa tutti gli allarmi per il giorno concluso"""
    pct_weapon = (weapon_count / total * 100) if total > 0 else 0
    
    # Lista di controlli: (Nome Metrica, Valore Corrente, Soglia Alarm, Soglia Warn, Unità)
    checks = [
        ("TOTALE CRIMINI", total, thresholds['total_alrm'], thresholds['total_warn'], ""),
        ("CRIMINI VIOLENTI", violent, thresholds['vio_alrm'], thresholds['vio_warn'], ""),
        ("PCT ARMA", pct_weapon, thresholds['weap_alrm'], thresholds['weap_warn'], "%")
    ]
    
    for name, val, alarm_th, warn_th, unit in checks:
        if val >= alarm_th:
            print(f"🚨 ALARM {day} | {name}: {val:.2f}{unit} (Soglia: {alarm_th:.2f}{unit})")
        elif val >= warn_th:
            print(f"⚠️  WARNING {day} | {name}: {val:.2f}{unit} (Soglia: {warn_th:.2f}{unit})")

# Dizionario soglie (presupponendo tu abbia calcolato le variabili prima come nel tuo script)
thresh_dict = {
    'total_warn': warn_total, 'total_alrm': alarm_total,
    'vio_warn': warn_violent, 'vio_alrm': alarm_violent,
    'weap_warn': warn_weapon_pct, 'weap_alrm': alarm_weapon_pct
}

# --- 2. CICLO DI CARICAMENTO OTTIMIZZATO ---
print("Inizio caricamento ottimizzato...")
start_time = time.time()

# Configura Batching (Cruciale!)
write_api = client.write_api(write_options=WriteOptions(batch_size=2000, flush_interval=1000))

# Variabili accumulatore
current_day = None
day_total = 0
day_violent = 0
day_weapon = 0
cnt_written = 0

# itertuples è ~100x più veloce di iterrows
for row in df.itertuples(index=True): # index=True mantiene l'indice originale per unicità
    
    # Accesso rapido alla data (è un attributo dell'oggetto, non lookup dizionario)
    row_date = row.DATE_OCC.date()

    # --- LOGICA CAMBIO GIORNO ---
    if row_date != current_day:
        # Processa il giorno precedente (se esiste)
        if current_day is not None:
            check_daily_alerts(current_day, day_total, day_violent, day_weapon, thresh_dict)
        
        # Reset contatori
        current_day = row_date
        day_total = 0
        day_violent = 0
        day_weapon = 0
    
    # --- AGGIORNAMENTO CONTATORI (Somma diretta booleani) ---
    day_total += 1
    day_violent += row.is_violent # True somma 1, False somma 0
    day_weapon += row.is_weapon

    # --- CREAZIONE POINT ---
    # Nota: row.Index usa l'indice del dataframe originale
    unique_ts = row.DATE_OCC + pd.Timedelta(microseconds=row.Index % 1_000_000)
    
    # Determina stringhe per i tag
    str_part = "1" if row.is_violent else "2"
    str_weapon = "True" if row.is_weapon else "False"
    
    point = Point("crime_report") \
        .tag("area_name", str(row.AREA_NAME)) \
        .tag("part", str_part) \
        .tag("weapon_flag", str_weapon) \
        .tag("season", get_season(row.DATE_OCC)) \
        .tag("time_period", get_day_night(row.TIME_OCC)) \
        .field("count", 1) \
        .field("lat", float(row.LAT)) \
        .field("lon", float(row.LON)) \
        .time(unique_ts, WritePrecision.US)

    # Campi opzionali (check rapido)
    # getattr è sicuro se la colonna esiste, altrimenti usa check standard
    if hasattr(row, 'Vict_Age') and row.Vict_Age > 0:
        point.field("vict_age", int(row.Vict_Age))

    write_api.write(bucket=bucket, org=org, record=point)
    cnt_written += 1

    if cnt_written % 100_000 == 0:
        print(f"...elaborati {cnt_written} record...")

# --- CHECK FINALE (Per non perdere l'ultimo giorno) ---
if current_day is not None:
    check_daily_alerts(current_day, day_total, day_violent, day_weapon, thresh_dict)

write_api.flush()
write_api.close()

print(f"Terminato in {time.time() - start_time:.2f} secondi. Totale scritti: {cnt_written}")