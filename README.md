# Sistemi Informativi Evoluti e Big Data

## Homework Repository – A.A. 2025-2026

**Autore**: Camossi Filippo (m. 734170)

Repository contenente i 4 homework del corso di Sistemi Informativi Evoluti e Big Data, focalizzati sull'utilizzo di database NoSQL e paradigmi di calcolo distribuito per l'analisi di Big Data.

---

## 📚 Struttura del Repository

```
SEBD_homework/
├── MongoDB/     # Homework #1 - Document Store
├── InfluxDB/    # Homework #2 - Time Series Database
├── Neo4j/       # Homework #3 - Graph Database
├── MapReduce/   # Homework #4 - Distributed Computing
└── README.md    # Questo file
```

---

## Homework #1 – MongoDB

**Obiettivo:** Analisi di recensioni di prodotti alimentari Amazon

### Contenuto
- Dataset: **Amazon Fine Food Reviews** (~568k recensioni)
- Caricamento dati in collezioni MongoDB organizzate per score
- **Sentiment Analysis** con VADER (ottimizzazione parametri)
- Query analitiche complesse con aggregation pipeline
- **Sistema di raccomandazione ibrido** (collaborative + content-based + sentiment)
- Analisi temporale dell'evoluzione del sentiment

### Tecnologie
`MongoDB` · `Python` · `VADER` · `scikit-learn` · `pandas`

[Vai all'homework MongoDB →](./MongoDB/)

---

## Homework #2 – InfluxDB

**Obiettivo:** Analisi di dati time-series sui crimini di Los Angeles

### Contenuto
- Dataset: **Crime Data from 2020 to Present** (Data.gov)
- Caricamento batch ottimizzato in InfluxDB
- Query analitiche con linguaggio **Flux**
- Visualizzazioni temporali e geografiche
- **Clustering incrementale** con libreria River

### Tecnologie
`InfluxDB` · `Flux` · `Python` · `River` · `pandas` · `matplotlib`

[Vai all'homework InfluxDB →](./InfluxDB/)

---

## Homework #3 – Neo4j

**Obiettivo:** Analisi di pubblicazioni scientifiche sull'Intelligenza Artificiale

### Contenuto
- Dataset: **ArXiv AI Papers** (paper, autori, topic)
- Modello a grafo: `Paper`, `Author`, `Topic` con relazioni
- Query Cypher per analisi di rete
- **Similarità di Ruzicka** (Jaccard pesata) tra paper
- Rete di co-authorship e percorsi minimi

### Tecnologie
`Neo4j` · `Cypher` · `Python` · `pandas` · `matplotlib`

[Vai all'homework Neo4j →](./Neo4j/)

---

## Homework #4 – MapReduce

**Obiettivo:** Analisi pedaggi autostradali con paradigma MapReduce

### Contenuto
- Dataset: **100.000 transiti autostradali** (generato con Faker)
- Confronto pedaggi 2015 vs 2025 (con inflazione 15-25%)
- Implementazione **mrjob** (Hadoop streaming)
- Implementazione **PySpark** (DataFrame API)
- Benchmark prestazioni: mrjob ~0.50s vs PySpark ~2.37s

### Tecnologie
`mrjob` · `PySpark` · `Python` · `Faker` · `Hadoop`

[Vai all'homework MapReduce →](./MapReduce/)

---

## Quick Start

### Prerequisiti Generali
- **Python 3.8+**
- **Jupyter Notebook** / JupyterLab
- Database specifici per ogni homework (MongoDB, InfluxDB, Neo4j)
- Apache Spark per Homework #4

### Setup

```bash
# Clone del repository
git clone <repository-url>
cd SEBD_homework

# Setup homework specifico
cd MongoDB  # o InfluxDB, Neo4j, MapReduce
pip install -r requirements.txt

# Avvio Jupyter (per notebook)
jupyter notebook
```

---

## Note

- Ogni homework è **completamente indipendente**
- Le dipendenze Python sono specificate in ogni cartella (`requirements.txt`)
- I dataset devono essere scaricati separatamente (vedi README specifici)
- Assicurarsi che i database NoSQL siano installati e in esecuzione

---

## Riepilogo Tecnologie

| Homework | Database/Framework | Paradigma | Dataset Size |
|----------|-------------------|-----------|--------------|
| #1 | MongoDB | Document Store | ~568k record |
| #2 | InfluxDB | Time Series | ~900k record |
| #3 | Neo4j | Graph Database | ~10k paper |
| #4 | mrjob + PySpark | MapReduce | 100k record |

---

## Licenza

Materiale didattico per uso accademico.