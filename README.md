# SEBD homework

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)
![InfluxDB](https://img.shields.io/badge/InfluxDB-22ADF6?style=flat-square&logo=influxdb&logoColor=white)
![Neo4j](https://img.shields.io/badge/Neo4j-018BFF?style=flat-square&logo=neo4j&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=flat-square&logo=apachespark&logoColor=white)

Four homework projects for the Advanced Information Systems and Big Data course (academic year 2025-2026), by Filippo Camossi. Each one runs the same kind of analysis on a different data model: document, time series, graph and MapReduce.

## Projects

| Project | Dataset | What it does |
| --- | --- | --- |
| [MongoDB](./MongoDB/) | Amazon Fine Food Reviews, about 568k reviews | Aggregation pipelines, VADER sentiment analysis with grid search, and a hybrid recommender (collaborative, TF-IDF content and sentiment) |
| [InfluxDB](./InfluxDB/) | Los Angeles crime data, about 900k records | Batch ingestion, Flux queries on time and area, and online clustering of locations with River |
| [Neo4j](./Neo4j/) | ArXiv AI papers | Graph of papers, authors and topics, Cypher analytics, co-authorship paths and weighted Jaccard (Ruzicka) topic similarity |
| [MapReduce](./MapReduce/) | Synthetic highway tolls, 100k records | Average toll per vehicle class in 2015 and 2025, implemented with mrjob and with PySpark |

Every folder is independent. It has its own README, `requirements.txt`, the assignment PDF and the written report (`*_Camossi.pdf`).

## Getting started

You need Python 3.8+, Jupyter, and the database for the project you want to run (MongoDB, InfluxDB 2.x or Neo4j). The MapReduce project needs Java 8+ for Spark.

```bash
git clone https://github.com/SickCiQuattro/SEBD_homework.git
cd SEBD_homework/MongoDB   # or InfluxDB, Neo4j, MapReduce
pip install -r requirements.txt
jupyter notebook
```

> [!NOTE]
> The MongoDB and InfluxDB datasets are too large for the repository. Each README links to where you can download them.
