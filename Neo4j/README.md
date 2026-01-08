# Homework #3 – Neo4j

## Artificial Intelligence Publication Trends

**Corso**: Sistemi Informativi Evoluti e Big Data – A.A. 2025-2026  
**Autore**: Camossi Filippo (m. 734170)

### Descrizione del Progetto

Questo progetto implementa un'analisi di pubblicazioni scientifiche sull'Intelligenza Artificiale utilizzando **Neo4j**, un database a grafo. L'obiettivo è modellare relazioni tra paper, autori e topic, calcolando metriche di similarità e analizzando reti di co-authorship.

### Dataset

**Artificial Intelligence Publication Trends** - ArXiv papers

File CSV:
- `arxiv_papers.csv`: Informazioni sugli articoli (titolo, abstract, data, autori)
- `papers_with_topics.csv`: Associazione paper-topic con probabilità
- `topic_definitions.csv`: Definizioni dei topic estratti

---

## Struttura dei File

```
Neo4j/
├── artificial_intelligence_publication_trends.ipynb  # Notebook principale
├── requirements.txt                                   # Dipendenze Python
├── README.md                                          # Questo file
├── Dataset/
│   ├── arxiv_papers.csv
│   ├── papers_with_topics.csv
│   ├── topic_definitions.csv
│   └── TopicExtractor.py
└── Images/                                            # Screenshot query Neo4j
    ├── Query1.png
    ├── Query4.png
    └── Query6.png
```

---

## Installazione

### 1. Prerequisiti

- **Python 3.8+**
- **Neo4j Desktop** o **Neo4j Community Server**
- **Jupyter Notebook**

### 2. Installazione Neo4j

**Neo4j Desktop (consigliato):**
Scarica da [neo4j.com/download](https://neo4j.com/download/)

**macOS (con Homebrew):**
```bash
brew install neo4j
neo4j start
```

**Docker:**
```bash
docker run -p 7474:7474 -p 7687:7687 neo4j:latest
```

### 3. Configurazione Neo4j

1. Avvia Neo4j e accedi a `http://localhost:7474`
2. Imposta username/password (default: `neo4j`/`neo4j`)
3. Aggiorna le credenziali nel notebook

### 4. Installazione Dipendenze Python

```bash
cd Neo4j
pip install -r requirements.txt
```

---

## Esecuzione

```bash
jupyter notebook artificial_intelligence_publication_trends.ipynb
```

---

## Modello del Grafo

### Nodi
- **Paper**: `{url, title, abstract, date}`
- **Author**: `{name}`
- **Topic**: `{id, name, keywords}`

### Relazioni
- `(:Author)-[:AUTHORED]->(:Paper)` - Autore ha scritto paper
- `(:Paper)-[:ON_TOPIC]->(:Topic)` - Paper tratta topic (con probabilità)
- `(:Author)-[:COAUTHORED_WITH]-(:Author)` - Co-authorship tra autori
- `(:Paper)-[:SIMILAR_TOPIC]-(:Paper)` - Similarità basata su topic

---

## Query Implementate

### Query 1: Schema del Database
Visualizzazione dello schema con `CALL db.schema.visualization()`

### Query 2: Top 5 Autori per Numero di Articoli
```cypher
MATCH (a:Author)-[:AUTHORED]->(p:Paper)
RETURN a.name AS author, COUNT(p) AS papers_count
ORDER BY papers_count DESC LIMIT 5
```

### Query 3: Andamento Temporale Pubblicazioni
Distribuzione dei paper nel tempo (per anno/mese)

### Query 4: Percorso Più Breve tra Due Autori
```cypher
MATCH (a1:Author {name: 'Xin Wang'}), (a2:Author {name: 'Yang Li'})
MATCH p = shortestPath((a1)-[:COAUTHORED_WITH*]-(a2))
RETURN p
```

### Query 5: Similarità tra Autori
Formula implementata:
$$Sim(a_1, a_2) = \frac{1}{|P_1| \cdot |P_2|} \sum_{p_i \in P_1} \sum_{p_j \in P_2} sim_{T}(p_i, p_j)$$

### Query 6: Rete Co-authorship Top 20 Autori
Visualizzazione del sottografo di collaborazione

---

## Algoritmi Implementati

### Similarità di Ruzicka (Jaccard Pesata)
Per calcolare la similarità tra paper basata sui topic:

$$sim_{T}(p,q) = \frac{\sum_{i \in U_T} \min(p_i, q_i)}{\sum_{i \in U_T} \max(p_i, q_i)}$$

Dove $p_i$ e $q_i$ sono le probabilità del topic $i$ per i paper $p$ e $q$.

---

## Tecnologie Utilizzate

| Tecnologia | Utilizzo |
|------------|----------|
| **Neo4j** | Database a grafo |
| **Cypher** | Linguaggio di query |
| **neo4j (Python)** | Driver ufficiale |
| **pandas** | Manipolazione dati |
| **matplotlib** | Visualizzazioni |

---

## Note Tecniche

- **Batch Size**: 1000 record per ottimizzare le scritture
- **Constraints**: Unicità su Paper.url, Author.name, Topic.id
- **Soglia Similarità**: 0.15 per relazioni SIMILAR_TOPIC
- I paper sono tutti del 2021 (dataset ArXiv specifico)
