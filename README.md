# Advanced Information Systems & Big Data (SEBD)

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)
![InfluxDB](https://img.shields.io/badge/InfluxDB-22ADF6?style=flat-square&logo=influxdb&logoColor=white)
![Neo4j](https://img.shields.io/badge/Neo4j-018BFF?style=flat-square&logo=neo4j&logoColor=white)
![Apache Spark](https://img.shields.io/badge/PySpark-E25A1C?style=flat-square&logo=apachespark&logoColor=white)

**Author:** Filippo Camossi
**Academic Year:** 2025-2026

## 📖 Portfolio Overview

This repository contains a collection of four distinct Big Data analytics projects developed for the _Advanced Information Systems and Big Data_ course. The portfolio explores the practical application of different **NoSQL databases** (Document, Time-Series, Graph) and **Distributed Computing paradigms** (MapReduce) on real-world and synthetic datasets.

The goal is to benchmark and compare data ingestion, complex querying, and machine learning integration (such as sentiment analysis, recommendation engines, and online clustering) across different technological stacks.

## 🗂️ Repository Structure & Projects

Each module is completely independent and contains its own specific documentation, source code, and Python requirements.

- 📦 **[Homework #1: MongoDB](./MongoDB/)**
    - **Domain:** E-commerce (Amazon Fine Food Reviews, ~568k records).
    - **Focus:** Document Store analytics, VADER Sentiment Analysis, and a Hybrid Recommendation System (Collaborative + Content-Based + Sentiment).
- 📈 **[Homework #2: InfluxDB](./InfluxDB/)**
    - **Domain:** Urban Security (Los Angeles Crime Data, ~900k records).
    - **Focus:** Time-Series Database management, Flux analytical queries, spatial-temporal pattern recognition, and Incremental/Online Clustering using `River`.
- 🕸️ **[Homework #3: Neo4j](./Neo4j/)**
    - **Domain:** Scientific Research (ArXiv AI Papers).
    - **Focus:** Graph Database modeling (Papers, Authors, Topics), Cypher queries, co-authorship network analysis, and weighted Jaccard (Ruzicka) similarity calculations.
- 🚀 **[Homework #4: MapReduce](./MapReduce/)**
    - **Domain:** Transportation (Highway Tolls, 100k records).
    - **Focus:** Distributed Computing benchmark. Compares a pure Python implementation (`mrjob` / Hadoop Streaming) against Spark's DataFrame API (`PySpark`) to calculate inflation trends over a decade.

## 🚀 Quick Start

### General Prerequisites

- **Python 3.8+**
- **Jupyter Notebook / JupyterLab**
- Specific database engines depending on the module (MongoDB, InfluxDB 2.x, Neo4j).
- Java 8+ (Required for PySpark in HW#4).

### Basic Setup

```bash
# Clone the repository
git clone [https://github.com/yourusername/SEBD_homework.git](https://github.com/yourusername/SEBD_homework.git)
cd SEBD_homework

# Navigate to a specific project module
cd MongoDB  # or InfluxDB, Neo4j, MapReduce

# Install specific dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook
```
