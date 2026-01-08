# Homework #4 – MapReduce

## Analisi dei Pedaggi Autostradali

### Descrizione del Progetto

Questo progetto implementa un'analisi MapReduce per calcolare il **pedaggio medio pagato da ogni tipo di veicolo** negli anni 2015 e 2025, evidenziando la variazione percentuale nel decennio.

### Dataset

Il dataset contiene i seguenti campi:

-   **IDVeicolo**: Identificativo univoco del veicolo (es. AB123CD)
-   **TipoVeicolo**: Categoria del veicolo (Auto, Moto, Camion, Autobus, Furgone)
-   **Tratta**: Tratta autostradale (es. A1-Milano-Bologna)
-   **Pedaggio**: Importo pagato in euro
-   **DataTransito**: Data nel formato GG/MM/YYYY
-   **FasciaOraria**: Fascia oraria (Mattina, Pomeriggio, Sera, Notte)
-   **Provincia**: Provincia del casello

---

## Struttura dei File

```
MapReduce/
├── DatasetGenerator.py     # Generatore del dataset
├── mapreduce_mrjob.py      # Implementazione mrjob
├── mapreduce_pyspark.py    # Implementazione PySpark
├── requirements.txt        # Dipendenze Python
├── README.md              # Questo file
└── caselli_autostradali.csv  # Dataset generato (dopo esecuzione)
```

---

## Installazione

```bash
# Installa le dipendenze
pip install -r requirements.txt
```

**Nota per PySpark**: Assicurarsi di avere Java 8 o 11 installato e la variabile `JAVA_HOME` configurata.

---

## Esecuzione

### 1. Generazione del Dataset

```bash
python DatasetGenerator.py
```

Genera il file `caselli_autostradali.csv` con 100.000 record.

### 2. Esecuzione mrjob

```bash
# Senza combiner
python mapreduce_mrjob.py caselli_autostradali.csv

# Con combiner (ottimizzato)
python mapreduce_mrjob.py caselli_autostradali.csv --use-combiner
```

### 3. Esecuzione PySpark

```bash
python mapreduce_pyspark.py
```

---

## Architettura MapReduce

### Flusso Logico

```
                    ┌─────────────────────────────────────────────────────────┐
                    │                      INPUT DATA                          │
                    │     caselli_autostradali.csv (100.000 records)          │
                    └─────────────────────────────────────────────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                    MAPPER                                        │
│  Input:  Linea CSV                                                              │
│  Output: (TipoVeicolo_Anno, (Pedaggio, 1))                                      │
│                                                                                 │
│  Esempio:                                                                       │
│  "AB123CD;Camion;A1-Milano-Bologna;25.50;15/03/2025;Mattina;Milano"            │
│                     ↓                                                           │
│  ("Camion_2025", (25.50, 1))                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              COMBINER (opzionale)                               │
│  Aggregazione locale per ridurre il traffico di rete                           │
│                                                                                 │
│  Input:  ("Camion_2025", [(25.50, 1), (30.20, 1), (28.00, 1)])                 │
│  Output: ("Camion_2025", (83.70, 3))                                           │
│                                                                                 │
│  ⚠️ Il combiner è applicabile perché la media può essere calcolata come:       │
│     media = Σ(pedaggi) / Σ(conteggi)                                           │
└─────────────────────────────────────────────────────────────────────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                   REDUCER                                        │
│  Calcola la media finale per ogni chiave                                        │
│                                                                                 │
│  Input:  ("Camion_2025", [(somma1, count1), (somma2, count2), ...])            │
│  Output: ("Camion_2025", {media: 24.78, transiti: 10234})                      │
└─────────────────────────────────────────────────────────────────────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          REDUCER STEP 2 (variazione)                            │
│  Raggruppa per tipo veicolo e calcola variazione percentuale                   │
│                                                                                 │
│  Output finale:                                                                 │
│  ("Camion", {media_2015: 20.32, media_2025: 24.78, variazione: +21.95%})       │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Considerazioni sulle Implementazioni

### Confronto mrjob vs PySpark

| Aspetto                | mrjob                       | PySpark                                        |
| ---------------------- | --------------------------- | ---------------------------------------------- |
| **Semplicità**         | ✅ Più semplice da scrivere | ⚠️ Richiede più setup                          |
| **Paradigma**          | MapReduce puro              | DataFrame + RDD + SQL                          |
| **Performance locale** | Buona per dataset piccoli   | Overhead iniziale, migliore per grandi dataset |
| **Scalabilità**        | Hadoop cluster              | Spark cluster (più veloce)                     |
| **Debug**              | Più difficile               | Migliore (Spark UI)                            |
| **Ottimizzazione**     | Manuale (combiner)          | Automatica (Catalyst optimizer)                |

### Considerazioni Qualitative

#### mrjob

-   **Pro**:
    -   Sintassi fedele al paradigma MapReduce originale
    -   Facile da comprendere per chi conosce Hadoop
    -   Leggero, poche dipendenze
-   **Contro**:
    -   Meno flessibile per analisi complesse
    -   Performance limitata in locale
    -   Debugging più complesso

#### PySpark

-   **Pro**:
    -   Tre modalità (DataFrame, RDD, SQL) per flessibilità
    -   Ottimizzazioni automatiche (lazy evaluation, catalyst optimizer)
    -   Caching dei dati intermedi
    -   Migliore per pipeline di analisi complesse
-   **Contro**:
    -   Overhead di inizializzazione JVM
    -   Maggiore consumo di memoria
    -   Configurazione più complessa

### Considerazioni Quantitative

Su un dataset di 100.000 record (esecuzione locale):

| Metodo                 | Tempo medio |
| ---------------------- | ----------- |
| mrjob (senza combiner) | ~8-12 sec   |
| mrjob (con combiner)   | ~6-9 sec    |
| PySpark DataFrame API  | ~3-5 sec    |
| PySpark RDD API        | ~4-6 sec    |
| PySpark SQL            | ~3-5 sec    |

**Nota**: I tempi possono variare significativamente in base all'hardware.

### Uso del Combiner

Il **combiner** è applicabile in questo caso perché la media può essere calcolata in modo incrementale:

$$\bar{x} = \frac{\sum_{i=1}^{n} x_i}{n}$$

Questo permette di aggregare parzialmente i dati:

-   **Senza combiner**: Tutti i record vengono inviati al reducer
-   **Con combiner**: Solo le somme parziali e i conteggi vengono inviati

In PySpark, `reduceByKey` funge automaticamente sia da combiner che da reducer.

---

## Risultati Attesi

L'output mostra:

1. **Media pedaggio 2015** per ogni tipo di veicolo
2. **Media pedaggio 2025** per ogni tipo di veicolo
3. **Variazione percentuale** (attesa: +15-25% per simulare l'inflazione)

Esempio output:

```
Tipo Veicolo      Media 2015    Media 2025    Variazione
─────────────────────────────────────────────────────────
Auto              €      8.23   €      9.89   +    20.17%
Autobus           €     14.12   €     16.94   +    19.97%
Camion            €     19.45   €     23.41   +    20.36%
Furgone           €     11.21   €     13.49   +    20.34%
Moto              €      5.52   €      6.63   +    20.11%
```

---

## Autore

Homework #4 - Sistemi per l'Elaborazione di Big Data (2024-2025)
