# Homework #4 – MapReduce

## Analisi dei Pedaggi Autostradali

**Corso**: Sistemi Informativi Evoluti e Big Data – A.A. 2025-2026  
**Autore**: Camossi Filippo (m. 734170)

### Descrizione del Progetto

Questo progetto implementa un'analisi MapReduce per calcolare il **pedaggio medio pagato da ogni tipo di veicolo** negli anni 2015 e 2025, evidenziando la variazione nel decennio.

### Dataset

Il dataset contiene i seguenti campi (separatore: virgola):

-   **IDVeicolo**: Targa del veicolo (es. AB123CD)
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
├── DatasetGenerator.py        # Generatore del dataset (Faker)
├── mapreduce_mrjob.py         # Implementazione mrjob
├── mapreduce_pyspark.py       # Implementazione PySpark
├── requirements.txt           # Dipendenze Python
├── README.md                  # Questo file
└── caselli_autostradali.csv   # Dataset generato (dopo esecuzione)
```

---

## Installazione

```bash
# Installa le dipendenze
pip install -r requirements.txt
```

**Nota per PySpark**: Assicurarsi di avere Java 8+ installato e la variabile `JAVA_HOME` configurata.

**Nota per Python 3.13**: Il file mrjob include una patch per compatibilità con il modulo deprecato `pipes`.

---

## Esecuzione

### 1. Generazione del Dataset

```bash
python DatasetGenerator.py
```

Genera il file `caselli_autostradali.csv` con 100.000 record.

### 2. Esecuzione mrjob

```bash
python mapreduce_mrjob.py caselli_autostradali.csv
```

### 3. Esecuzione PySpark

```bash
python mapreduce_pyspark.py
```

---

## Architettura MapReduce

### Flusso Logico (mrjob)

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
│  Output: (TipoVeicolo, [count_2015, sum_2015, count_2025, sum_2025])            │
│                                                                                 │
│  Esempio (record 2025):                                                         │
│  "AB123CD,Camion,A1-Milano-Bologna,25.50,15/03/2025,Mattina,Milano"             │
│                     ↓                                                           │
│  ("Camion", [0, 0.0, 1, 25.50])                                                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                   COMBINER                                       │
│  Aggregazione locale per ridurre il traffico di rete                            │
│                                                                                 │
│  Input:  ("Camion", [[0,0,1,25.5], [0,0,1,30.2], [1,20.1,0,0]])                │
│  Output: ("Camion", [1, 20.1, 2, 55.7])                                        │
│                                                                                 │
│  ⚠️ Il combiner è applicabile perché: media = Σ(pedaggi) / Σ(conteggi)         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                   REDUCER                                        │
│  Aggregazione finale e calcolo medie + variazione                               │
│                                                                                 │
│  Input:  ("Camion", [[c15, s15, c25, s25], ...])                               │
│  Output: ("Camion", {Media_2015: 20.15, Media_2025: 23.89, Variazione: 3.74})  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Risultati Ottenuti

Output dell'analisi su 100.000 record:

| Tipo Veicolo | Media 2015 (€) | Media 2025 (€) | Variazione (€) | Var. % |
| ------------ | -------------- | -------------- | -------------- | ------ |
| Camion       | 20.15          | 23.89          | +3.74          | +18.6% |
| Autobus      | 14.50          | 17.32          | +2.82          | +19.4% |
| Furgone      | 11.47          | 13.77          | +2.30          | +20.1% |
| Auto         | 8.48           | 10.23          | +1.75          | +20.6% |
| Moto         | 5.76           | 6.94           | +1.18          | +20.5% |

I dati riflettono correttamente l'inflazione simulata del 15-25% sui pedaggi del 2025.

---

## Confronto Implementazioni

### Analisi Quantitativa (100.000 record, esecuzione locale)

| Implementazione | Tempo      | Note                                |
| --------------- | ---------- | ----------------------------------- |
| **mrjob**       | **0.50 s** | Python puro, avvio immediato        |
| **PySpark**     | **2.37 s** | Overhead inizializzazione JVM (~2s) |

**Osservazione**: Su dataset di piccole dimensioni, mrjob risulta ~5x più veloce per l'assenza di overhead JVM. PySpark mostrerebbe vantaggi su dataset dell'ordine dei GB/TB in ambiente distribuito.

### Analisi Qualitativa

| Aspetto             | mrjob                           | PySpark                         |
| ------------------- | ------------------------------- | ------------------------------- |
| **Paradigma**       | Imperativo (Map/Combine/Reduce) | Dichiarativo (DataFrame API)    |
| **Combiner**        | Esplicito nel codice            | Automatico (Catalyst optimizer) |
| **Linee di codice** | ~80                             | ~65                             |
| **Leggibilità**     | Richiede comprensione MR        | Più intuitivo (SQL-like)        |
| **Scalabilità**     | Hadoop cluster                  | Spark cluster (in-memory)       |
| **Debug**           | Output testuale                 | Spark UI                        |

### Uso del Combiner

Il **combiner** è implementato esplicitamente in mrjob usando un vettore `[count_2015, sum_2015, count_2025, sum_2025]`:

```python
def combiner(self, key, values):
    c15, s15, c25, s25 = 0, 0.0, 0, 0.0
    for v in values:
        c15 += v[0]; s15 += v[1]
        c25 += v[2]; s25 += v[3]
    yield key, [c15, s15, c25, s25]
```

Questo è possibile perché la media è calcolabile come:

$$\bar{x} = \frac{\sum_{i=1}^{n} x_i}{n}$$

In PySpark, l'ottimizzazione equivalente è gestita automaticamente dall'optimizer Catalyst tramite `HashAggregate`.

---

## Note Tecniche

-   **Precisione floating-point**: Lieve differenza nella variazione Moto (1.17 in mrjob vs 1.18 in PySpark) dovuta alla diversa gestione dell'arrotondamento.
-   **Patch Python 3.13**: mrjob richiede il modulo deprecato `pipes`, sostituito con `shlex`.
-   **Dataset realistico**: Generato con libreria Faker (targhe e città italiane).
