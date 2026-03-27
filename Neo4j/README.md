# Homework #3 - Neo4j

## Artificial Intelligence Publication Trends

Course: Advanced Information Systems and Big Data (SEBD) - Academic Year 2025-2026  
Author: Filippo Camossi

## Project Overview

This module models and analyzes AI publication data from ArXiv with Neo4j.
It focuses on graph relationships among papers, authors, and topics, including co-authorship structures and similarity metrics.

## Goals

- Build a graph model for papers, authors, and topics.
- Query publication trends and author productivity with Cypher.
- Analyze co-authorship connectivity and shortest paths.
- Compute weighted Jaccard (Ruzicka) topic similarity between papers/authors.

## Tech Stack

- Python 3.8+
- Neo4j Desktop or Neo4j Server
- Cypher query language
- Jupyter Notebook
- neo4j Python driver, pandas, matplotlib

## Repository Structure

```text
Neo4j/
|- artificial_intelligence_publication_trends.ipynb
|- Dataset/
|  |- arxiv_papers.csv
|  |- papers_with_topics.csv
|  |- topic_definitions.csv
|  `- TopicExtractor.py
|- Images/
|- requirements.txt
`- README.md
```

## Setup

1. Install and start Neo4j.

macOS (Homebrew):

```bash
brew install neo4j
neo4j start
```

Alternative: Neo4j Desktop or Docker image.

2. Open Neo4j Browser at http://localhost:7474 and configure credentials.

3. Install Python dependencies:

```bash
cd Neo4j
pip install -r requirements.txt
```

## Run Locally

```bash
jupyter notebook artificial_intelligence_publication_trends.ipynb
```

Recommended notebook flow:

1. Data loading and graph population
2. Schema and constraints
3. Cypher analytics (authors, trends, connectivity)
4. Similarity calculations and graph visual outputs

## Key Implemented Features

- Graph schema with Paper, Author, Topic nodes.
- Core relations: AUTHORED, ON_TOPIC, COAUTHORED_WITH, SIMILAR_TOPIC.
- Top-author and trend queries.
- Co-authorship shortest path analysis.
- Topic-based similarity analysis using weighted Jaccard.

## Notable Technical Choices

- Constraints on identifiers (for example paper URL and author name) support consistent ingestion.
- Similarity edges are filtered with a threshold to avoid noisy links.
- The Ruzicka metric was chosen to compare probabilistic topic vectors.

## Similarity Formula

Weighted Jaccard (Ruzicka) used for topic vectors:

sim_T(p, q) = sum_i min(p_i, q_i) / sum_i max(p_i, q_i)

## Expected Outcome

After full execution you should obtain:

- A populated Neo4j graph of papers/authors/topics.
- Cypher query results for productivity and trend analysis.
- Co-authorship network insights and shortest paths.
- Similarity links derived from topic distributions.

## Troubleshooting

- If authentication fails, verify credentials in notebook connection settings.
- If import is slow, run writes in batches and check constraints before loading.
- If query complexity is high, limit result sets during visual exploration.

## Related Docs

- Root portfolio: ../README.md
- Neo4j docs: https://neo4j.com/docs/
- Cypher manual: https://neo4j.com/docs/cypher-manual/current/
