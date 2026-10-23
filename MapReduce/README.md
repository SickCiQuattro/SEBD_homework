# MapReduce: highway tolls

Computes the average toll per vehicle class in 2015 and 2025 from a synthetic dataset of 100,000 toll records, and compares two implementations: mrjob (Hadoop Streaming style) and PySpark. Homework #4 for the SEBD course.

## What it does

- `DatasetGenerator.py` builds `caselli_autostradali.csv` with Faker.
- `mapreduce_mrjob.py` emits `(vehicle_type, [count_2015, sum_2015, count_2025, sum_2025])` from the mapper, combines partial results locally, and computes averages and the decade variation in the reducer. The combiner cuts shuffle traffic, and carrying count and sum together keeps the averages correct.
- `mapreduce_pyspark.py` does the same aggregation with the DataFrame API and lets Catalyst optimize it.
- Both report the absolute and percentage change per vehicle class, and the runtime of each approach.

## Requirements

- Python 3.8+
- Java 8+ with `JAVA_HOME` set (needed by Spark)

## Usage

```bash
pip install -r requirements.txt

python DatasetGenerator.py
python mapreduce_mrjob.py caselli_autostradali.csv
python mapreduce_pyspark.py
```

> [!NOTE]
> `mapreduce_mrjob.py` includes a compatibility patch for the removed `pipes` module on Python 3.13.

## Troubleshooting

- PySpark fails to start: check the Java install and `JAVA_HOME`.
- CSV missing: run `DatasetGenerator.py` first.

## Files

- `MapReduce_Camossi.pdf`: written report
- `Homework_MapReduce_2025.2026.pdf`: assignment
