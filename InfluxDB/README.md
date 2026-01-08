# Homework #2 – InfluxDB

## Analisi dei Dati Criminali di Los Angeles

**Corso**: Sistemi Informativi Evoluti e Big Data – A.A. 2025-2026  
**Autore**: Camossi Filippo (m. 734170)

### Descrizione del Progetto

Questo progetto implementa un'analisi di dati time-series sui crimini di Los Angeles utilizzando **InfluxDB**, un database ottimizzato per serie temporali. L'obiettivo è analizzare pattern temporali, distribuzioni geografiche e applicare tecniche di clustering incrementale.

### Dataset

**Crime Data from 2020 to Present** - [Data.gov](https://catalog.data.gov/dataset/crime-data-from-2020-to-present)

Campi principali:
- **DR_NO**: Numero identificativo del report
- **Date Rptd / DATE OCC**: Data di segnalazione / occorrenza
- **TIME OCC**: Ora del crimine
- **AREA / AREA NAME**: Codice e nome dell'area
- **Crm Cd / Crm Cd Desc**: Codice e descrizione del crimine
- **Vict Age / Vict Sex**: Età e sesso della vittima
- **LAT / LON**: Coordinate geografiche

---

## Struttura dei File

```
InfluxDB/
├── los_angeles_crime_data.ipynb   # Notebook principale
├── Crime_Data_from_2020_to_Present.csv  # Dataset
├── requirements.txt               # Dipendenze Python
├── README.md                      # Questo file
└── weather_data/                  # Dataset meteo (opzionale)
```

---

## Installazione

### 1. Prerequisiti

- **Python 3.8+**
- **InfluxDB 2.x** (in esecuzione su `localhost:8086`)
- **Jupyter Notebook**

### 2. Installazione InfluxDB

**macOS (con Homebrew):**
```bash
brew install influxdb
brew services start influxdb
```

**Linux:**
```bash
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.7.1-linux-amd64.tar.gz
tar xvzf influxdb2-2.7.1-linux-amd64.tar.gz
./influxdb2-2.7.1-linux-amd64/influxd
```

**Windows:**
Scarica l'installer da [influxdata.com](https://portal.influxdata.com/downloads/)

### 3. Configurazione InfluxDB

1. Accedi a `http://localhost:8086`
2. Crea un'organizzazione (es. `unibs`)
3. Crea un bucket (es. `crime_data`)
4. Genera un API token e aggiornalo nel notebook

### 4. Download Dataset

Scarica il dataset da Data.gov:
- Link: https://catalog.data.gov/dataset/crime-data-from-2020-to-present
- Posiziona il file `Crime_Data_from_2020_to_Present.csv` nella cartella `InfluxDB/`

### 5. Installazione Dipendenze Python

```bash
cd InfluxDB
pip install -r requirements.txt
```

---

## Esecuzione

```bash
jupyter notebook los_angeles_crime_data.ipynb
```

Esegui le celle in ordine per:
1. Connessione a InfluxDB e caricamento dati
2. Query analitiche con Flux
3. Visualizzazioni temporali
4. Clustering incrementale con River

---

## Funzionalità Implementate

### 1. Caricamento Dati in InfluxDB
- Batch writing ottimizzato (5000 punti/batch)
- Gestione errori e retry automatico
- Reset bucket per ambiente pulito

### 2. Query Analitiche (Flux)
- Distribuzione crimini per area
- Andamento temporale (giornaliero/mensile)
- Analisi per tipo di crimine
- Fasce orarie più critiche

### 3. Visualizzazioni
- Serie temporali con matplotlib
- Heatmap geografiche
- Grafici a barre per distribuzioni

### 4. Clustering Incrementale
- Algoritmo online con libreria River
- Clustering su coordinate geografiche
- Analisi pattern spaziali dei crimini

---

## Tecnologie Utilizzate

| Tecnologia | Utilizzo |
|------------|----------|
| **InfluxDB 2.x** | Database time-series |
| **Flux** | Linguaggio di query |
| **influxdb-client** | Client Python |
| **River** | Machine Learning incrementale |
| **pandas** | Manipolazione dati |
| **matplotlib** | Visualizzazioni |

---

## Note Tecniche

- **Batch Size**: 5000 punti per ottimizzare le scritture
- **Timeout**: 30 secondi per query complesse
- **Flush Interval**: 10 secondi per auto-flush
- Il dataset completo contiene ~900k record
