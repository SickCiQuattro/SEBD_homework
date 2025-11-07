# Homework #1 - MongoDB

## Amazon Fine Food Reviews Analysis

Analisi completa del dataset Amazon Fine Food Reviews utilizzando MongoDB come database NoSQL per storage, aggregazione e analisi di grandi volumi di recensioni.

---

## 📋 Descrizione del Progetto

Questo homework implementa un sistema completo di analisi delle recensioni che include:

1. **Caricamento e Organizzazione Dati**

    - Import di ~568k recensioni in MongoDB
    - Organizzazione in 6 collezioni separate per livello di score (1-5 + no_text)
    - Struttura documento ottimizzata per query analitiche

2. **Sentiment Analysis con VADER**

    - Analisi automatica del sentiment (positive/neutral/negative)
    - Ottimizzazione parametri tramite grid search
    - Accuracy migliorata rispetto ai parametri default

3. **Query Analitiche**

    - Distribuzione recensioni per score
    - Top 5 prodotti con media score più alta
    - Top 5 utenti più attivi
    - Analisi correlazione score-sentiment
    - Prodotti con alto score ma sentiment negativo

4. **Sistema di Raccomandazione Ibrido**

    - Collaborative Filtering (co-occorrenza utenti)
    - Content-Based Filtering (TF-IDF similarity)
    - Sentiment-Based Filtering (qualità)
    - Score combinato pesato

5. **Analisi Temporale Avanzata**
    - Evoluzione mensile del sentiment
    - Rilevamento automatico anomalie
    - Visualizzazioni multi-linea
    - Discussione adattamento sistema di raccomandazione

---

## 🗂️ Struttura File

```
MongoDB/
├── amazon_fine_food_reviews.ipynb    # Notebook principale
├── Reviews.csv                        # Dataset (da scaricare)
├── requirements.txt                   # Dipendenze Python
└── README.md                          # Questo file
```

---

## 🛠️ Setup e Installazione

### 1. Prerequisiti

-   **Python 3.8+**
-   **MongoDB** (installato e in esecuzione su `localhost:27017`)
-   **Jupyter Notebook**

#### Installazione MongoDB

**macOS (con Homebrew):**

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**Windows:**
Scarica l'installer da [mongodb.com](https://www.mongodb.com/try/download/community)

### 2. Download Dataset

Scarica il dataset da Kaggle:

-   Link: https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews
-   File necessario: `Reviews.csv`
-   Posiziona il file nella cartella `MongoDB/`

### 3. Installazione Dipendenze Python

```bash
cd MongoDB
pip install -r requirements.txt
```

### 4. Avvio Notebook

```bash
jupyter notebook amazon_fine_food_reviews.ipynb
```

---

## 🚀 Esecuzione

1. **Verifica MongoDB in esecuzione:**

    ```bash
    # Verifica che MongoDB sia attivo
    mongosh  # oppure mongo
    ```

2. **Esegui le celle del notebook in ordine:**
    - Setup e import librerie
    - Caricamento dati in MongoDB
    - Ottimizzazione parametri VADER (opzionale ma raccomandato)
    - Sentiment analysis
    - Query analitiche
    - Sistema di raccomandazione
    - Analisi temporale

⏱️ **Tempo stimato:** ~30-45 minuti (incluso caricamento dati)

---

## 📊 Dataset

**Amazon Fine Food Reviews**

-   **Fonte:** Kaggle
-   **Dimensione:** ~568,000 recensioni
-   **Periodo:** Ottobre 1999 - Ottobre 2012
-   **Campi principali:**
    -   `ProductId`: ID prodotto
    -   `UserId`: ID utente
    -   `ProfileName`: Nome profilo utente
    -   `Score`: Valutazione 1-5 stelle
    -   `Summary`: Titolo recensione
    -   `Text`: Testo completo recensione
    -   `Time`: Timestamp Unix

---

## 🎯 Risultati Attesi

Dopo l'esecuzione completa del notebook, avrai:

✅ Database MongoDB popolato con recensioni organizzate  
✅ Parametri VADER ottimizzati per questo dominio specifico  
✅ Analisi statistiche complete con visualizzazioni  
✅ Sistema di raccomandazione funzionante  
✅ Report su evoluzione temporale del sentiment  
✅ Discussione approfondita su design choices (collezioni multiple vs singola)

---

## 📈 Metriche di Performance

**Sentiment Analysis (con parametri ottimizzati):**

-   Accuracy: ~80-85% (rispetto a ground truth basato su score)
-   Precision/Recall bilanciati per tutte le classi
-   Miglioramento ~5-10% rispetto a parametri default VADER

**Sistema di Raccomandazione:**

-   Tipo: Ibrido (Collaborative + Content-Based + Sentiment)
-   Pesi: 40% collaborative, 30% content, 30% sentiment
-   Top-N recommendations con score combinato

---

## 🔍 Query MongoDB Interessanti

Alcune query MongoDB utilizzate nel progetto:

```javascript
// Top prodotti per media score
db.score_5.aggregate([
    { $group: { _id: "$product_id", avg_score: { $avg: "$score" } } },
    { $sort: { avg_score: -1 } },
    { $limit: 5 },
]);

// Distribuzione sentiment per score
db.score_4.aggregate([{ $group: { _id: "$sentiment", count: { $sum: 1 } } }]);
```

---

## 📚 Dipendenze Principali

-   **pymongo**: Connessione e operazioni MongoDB
-   **pandas**: Manipolazione e analisi dati
-   **vaderSentiment**: Analisi sentiment
-   **scikit-learn**: TF-IDF e cosine similarity
-   **matplotlib/seaborn**: Visualizzazioni

Vedi `requirements.txt` per la lista completa.

---

## 🐛 Troubleshooting

### MongoDB non si connette

```bash
# Verifica che MongoDB sia in esecuzione
brew services list  # macOS
sudo systemctl status mongodb  # Linux

# Avvia MongoDB se necessario
brew services start mongodb-community  # macOS
sudo systemctl start mongodb  # Linux
```

### Dataset non trovato

-   Assicurati che `Reviews.csv` sia nella stessa directory del notebook
-   Verifica che il nome file sia esattamente `Reviews.csv`

### Errori di memoria

-   Il caricamento completo richiede ~2-3GB RAM
-   Riduci `sample_size_per_score` nell'ottimizzazione VADER se necessario

---

## 📖 Documentazione Aggiuntiva

-   [MongoDB Documentation](https://docs.mongodb.com/)
-   [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
-   [Dataset su Kaggle](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews)

---

## 💡 Possibili Estensioni

-   Implementazione indici MongoDB per ottimizzare le query
-   Sistema di raccomandazione con apprendimento online
-   Topic modeling (LDA) per identificare temi nelle recensioni
-   Dashboard interattiva con Streamlit o Dash
-   Analisi di network degli utenti (graph analysis)

---

## 👨‍💻 Autore

Filippo Camossi  
A.A. 2025-2026

---

[← Torna al README principale](../README.md)
