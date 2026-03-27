# Homework #4 - MapReduce

## Highway Toll Analytics (mrjob vs PySpark)

Course: Advanced Information Systems and Big Data (SEBD) - Academic Year 2025-2026  
Author: Filippo Camossi

## Project Overview

This module analyzes synthetic highway toll data to compute the average toll by vehicle type in 2015 and 2025.
It also benchmarks two distributed-computing approaches: a classic MapReduce pipeline with mrjob and a PySpark DataFrame implementation.

## Goals

- Generate a realistic toll dataset with 100,000 records.
- Compute per-vehicle averages for 2015 and 2025.
- Measure decade variation and inflation-like trend.
- Compare implementation style and execution overhead (mrjob vs PySpark).

## Tech Stack

- Python 3.8+
- mrjob (Hadoop Streaming style)
- PySpark (DataFrame API)
- Faker (synthetic dataset generation)
- Java 8+ (required by Spark)

## Repository Structure

```text
MapReduce/
|- DatasetGenerator.py
|- mapreduce_mrjob.py
|- mapreduce_pyspark.py
|- caselli_autostradali.csv
|- requirements.txt
`- README.md
```

## Setup

Install dependencies:

```bash
cd MapReduce
pip install -r requirements.txt
```

Environment notes:

- PySpark requires Java 8+ and `JAVA_HOME` configured.
- The mrjob script includes a compatibility fix for Python 3.13 (`pipes` replacement).

## Run Locally

1. Generate dataset:

```bash
python DatasetGenerator.py
```

2. Run mrjob pipeline:

```bash
python mapreduce_mrjob.py caselli_autostradali.csv
```

3. Run PySpark implementation:

```bash
python mapreduce_pyspark.py
```

## Key Implemented Features

- Synthetic but realistic transport dataset generation.
- Mapper/Combiner/Reducer pipeline for grouped averages.
- Equivalent PySpark DataFrame aggregation flow.
- Side-by-side runtime comparison and qualitative trade-off analysis.

## Notable Technical Choices

- Combiner is explicitly used in mrjob to reduce shuffle traffic.
- Aggregation tracks both count and sum for each year to preserve average correctness.
- Spark implementation delegates optimization to Catalyst for grouped aggregations.

## MapReduce Logic Summary

- Mapper emits: `(vehicle_type, [count_2015, sum_2015, count_2025, sum_2025])`
- Combiner performs local partial aggregation.
- Reducer computes final averages and variation by vehicle class.

Average formula:

mean = sum(values) / count(values)

## Expected Outcome

After running both implementations you should obtain:

- Average toll values by vehicle class for 2015 and 2025.
- Absolute and percentage variation over the decade.
- Runtime comparison showing overhead differences in local execution.

## Troubleshooting

- If PySpark fails, verify Java installation and `JAVA_HOME`.
- If CSV is missing, run `DatasetGenerator.py` first.
- If mrjob behavior changes on newer Python versions, use the included compatibility patch.

## Related Docs

- Root portfolio: ../README.md
- mrjob docs: https://mrjob.readthedocs.io/
- Spark docs: https://spark.apache.org/docs/latest/
