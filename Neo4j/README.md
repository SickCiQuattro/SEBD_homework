# Neo4j: AI publication trends

Graph analysis of ArXiv AI papers in Neo4j. Homework #3 for the SEBD course.

## What it does

- Models papers, authors and topics as nodes, linked by `AUTHORED`, `ON_TOPIC`, `COAUTHORED_WITH` and `SIMILAR_TOPIC`.
- Uses constraints on paper URL and author name to keep ingestion consistent.
- Queries publication trends and top authors with Cypher.
- Finds shortest co-authorship paths between authors.
- Adds `SIMILAR_TOPIC` edges above a threshold, using weighted Jaccard (Ruzicka) similarity on topic vectors:

```text
sim(p, q) = sum_i min(p_i, q_i) / sum_i max(p_i, q_i)
```

`Dataset/TopicExtractor.py` runs BERTopic on `arxiv_papers.csv` and writes `papers_with_topics.csv` and `topic_definitions.csv`. It needs `bertopic` and `sentence-transformers`, which are not in `requirements.txt`; the generated CSVs are already included.

## Requirements

- Python 3.8+
- Neo4j (Desktop, server or Docker) on `bolt://localhost:7687`

## Usage

```bash
brew install neo4j
neo4j start

pip install -r requirements.txt
export NEO4J_PASSWORD=<your-password>
jupyter notebook artificial_intelligence_publication_trends.ipynb
```

Set the password in Neo4j Browser (http://localhost:7474) first. The notebook runs in order: graph population, schema and constraints, Cypher analytics, similarity.

## Troubleshooting

- Authentication errors: check that `NEO4J_PASSWORD` matches the database password.
- Slow import: load in batches and create the constraints before loading.
- Heavy queries: limit the result size while exploring.

## Files

- `artificial_intelligence_publication_trends.ipynb`: the full pipeline
- `Images/`: screenshots of query results
- `Neo4j_Camossi.pdf`: written report
- `Homework_Neo4J_2025.2026.pdf`: assignment
