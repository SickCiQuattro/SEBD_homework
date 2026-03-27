# Homework #2 - InfluxDB

## Los Angeles Crime Time-Series Analytics

Course: Advanced Information Systems and Big Data (SEBD) - Academic Year 2025-2026  
Author: Filippo Camossi

## Project Overview

This module analyzes Los Angeles crime data with InfluxDB as a time-series database.
The objective is to combine temporal querying, spatial insights, and incremental machine learning for urban pattern analysis.

## Goals

- Ingest high-volume event data into InfluxDB 2.x.
- Query and aggregate with Flux for temporal and categorical trends.
- Produce visual summaries for area/time crime dynamics.
- Apply online clustering with River on geographic signals.

## Tech Stack

- Python 3.8+
- InfluxDB 2.x (localhost:8086)
- Flux query language
- Jupyter Notebook
- influxdb-client, pandas, matplotlib, River

## Repository Structure

```text
InfluxDB/
|- los_angeles_crime_data.ipynb
|- Crime_Data_from_2020_to_Present.csv
|- weather_data/
|- requirements.txt
`- README.md
```

## Setup

1. Install and start InfluxDB.

macOS (Homebrew):

```bash
brew install influxdb
brew services start influxdb
```

2. Open the InfluxDB UI at http://localhost:8086 and configure:

- organization (for example: `unibs`)
- bucket (for example: `crime_data`)
- API token

3. Download dataset and place it in this folder:
https://catalog.data.gov/dataset/crime-data-from-2020-to-present

4. Install Python dependencies:

```bash
cd InfluxDB
pip install -r requirements.txt
```

## Run Locally

```bash
jupyter notebook los_angeles_crime_data.ipynb
```

Notebook flow:

1. Connection and write pipeline
2. Flux analytical queries
3. Time-series and distribution visualizations
4. Incremental clustering with River

## Key Implemented Features

- Optimized batch ingestion (5,000 points per write batch).
- Flux-based analysis by area, crime type, time windows, and critical hours.
- Time and geo-oriented visual exploration.
- Online clustering to detect evolving spatial crime patterns.

## Notable Technical Choices

- Batch writes are tuned to balance throughput and reliability.
- Query timeout/flush settings are configured to handle heavier operations.
- Incremental modeling enables updates without full retraining.

## Expected Outcome

After full execution you should obtain:

- InfluxDB bucket populated with crime events.
- Reproducible temporal and categorical analytical views.
- Visual insights on crime concentration and variation.
- Incremental clustering outputs on geographic data.

## Troubleshooting

- If connection fails, verify InfluxDB is running and token/org/bucket are correct.
- If writes are slow, reduce batch size in the notebook and retry.
- If query times out, simplify time ranges or increase timeout configuration.

## Related Docs

- Root portfolio: ../README.md
- InfluxDB docs: https://docs.influxdata.com/
- River docs: https://riverml.xyz/
