# Sistemi Informativi Evoluti e Big Data

## Homework - A.A. 2025-2026

Repository contenente gli homework del corso di Sistemi Informativi Evoluti e Big Data, focalizzati sull'utilizzo di database NoSQL per l'analisi di big data.

---

## 📚 Struttura del Repository

Il repository è organizzato in cartelle separate per ogni homework, ciascuna dedicata a un diverso database NoSQL:

```
SEBD_homework/
│
├── MongoDB/              # Homework #1 - MongoDB
├── InfluxDB/            # Homework #2 - InfluxDB (coming soon)
└── TBD/                 # Homework #3 - TBD
```

---

## 🗃️ Homework #1 - MongoDB

**Obiettivo:** Analisi di recensioni di prodotti alimentari Amazon utilizzando MongoDB per storage e aggregazione dati.

### Contenuto

-   Dataset: [Amazon Fine Food Reviews](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews)
-   **Caricamento dati** in collezioni MongoDB organizzate per score
-   **Sentiment Analysis** con VADER (ottimizzazione parametri)
-   **Query analitiche** complesse con aggregation pipeline
-   **Sistema di raccomandazione ibrido** (collaborative + content-based + sentiment)
-   **Analisi temporale** dell'evoluzione del sentiment

### Tecnologie

-   MongoDB (NoSQL Document Store)
-   Python (pandas, pymongo, scikit-learn)
-   VADER Sentiment Analysis
-   Jupyter Notebook

### File Principali

-   `amazon_fine_food_reviews.ipynb` - Notebook principale
-   `Reviews.csv` - Dataset (da scaricare da Kaggle)
-   `requirements.txt` - Dipendenze Python

📖 [Vai all'homework MongoDB →](./MongoDB/)

---

## 📊 Homework #2 - InfluxDB

**Obiettivo:** Analisi di dati time-series utilizzando InfluxDB.

### Stato

🚧 **Coming Soon** - In fase di sviluppo

### Tecnologie Previste

-   InfluxDB (Time Series Database)
-   Python
-   Jupyter Notebook

---

## 🔮 Homework #3 - TBD

**Obiettivo:** Da definire

### Stato

📝 **Planned** - Database NoSQL da determinare

---

## 🚀 Quick Start

### Prerequisiti Generali

-   Python 3.8 o superiore
-   Jupyter Notebook / JupyterLab
-   MongoDB (per Homework #1)
-   InfluxDB (per Homework #2)

### Setup Ambiente

1. **Clone del repository**

    ```bash
    git clone <repository-url>
    cd SEBD_homework
    ```

2. **Setup Homework specifico**

    ```bash
    cd MongoDB  # o InfluxDB, etc.
    pip install -r requirements.txt
    ```

3. **Avvio Jupyter**
    ```bash
    jupyter notebook
    ```

---

## 📝 Note

-   Ogni homework è completamente indipendente
-   Le dipendenze Python sono specificate in ogni cartella
-   I dataset devono essere scaricati separatamente (vedi README specifici)
-   Assicurarsi che i database NoSQL siano installati e in esecuzione

---

## 👨‍💻 Autore

Filippo Camossi  
Corso: Sistemi Informativi Evoluti e Big Data  
A.A. 2025-2026

---

## 📄 Licenza

Materiale didattico per uso accademico.
