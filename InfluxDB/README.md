# InfluxDB: Los Angeles crime data

Time-series analysis of Los Angeles crime records (about 900k) using InfluxDB 2.x. Homework #2 for the SEBD course.

## What it does

- Writes the dataset to InfluxDB in batches of 5,000 points.
- Uses Flux to aggregate crimes by area, crime type, time window and critical hours.
- Plots crime over time and by location.
- Clusters crime locations with River, which updates the model one record at a time instead of retraining.

## Requirements

- Python 3.8+
- InfluxDB 2.x running on `localhost:8086`, with an organization (the notebook uses `unibs`), a bucket (`crime_data`) and an API token
- `Crime_Data_from_2020_to_Present.csv` from [data.gov](https://catalog.data.gov/dataset/crime-data-from-2020-to-present), placed in this folder

## Usage

```bash
brew install influxdb
brew services start influxdb

pip install -r requirements.txt
export INFLUXDB_TOKEN=<your-token>
jupyter notebook los_angeles_crime_data.ipynb
```

The notebook runs in order: connection and write pipeline, Flux queries, visualizations, incremental clustering.

> [!WARNING]
> The token is read from the `INFLUXDB_TOKEN` environment variable. Do not paste it into the notebook.

## Troubleshooting

- Connection errors: check that InfluxDB is running and that the token, organization and bucket match.
- Slow writes: lower the batch size in the notebook.
- Query timeouts: narrow the time range or raise the client timeout.

## Files

- `los_angeles_crime_data.ipynb`: the full pipeline
- `InfluxDB_Camossi.pdf`: written report
- `Homework_InfluxDB_2025.2026.pdf`: assignment
