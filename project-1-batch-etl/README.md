# Project 1: Batch ETL Pipeline (NYC Taxi Data)

An end-to-end batch ETL pipeline that ingests NYC Yellow Taxi trip data, cleans and transforms it, loads it into PostgreSQL, and orchestrates the whole workflow with Apache Airflow.

## Architecture
```
Airflow DAG  ->  extract  ->  transform  ->  load  ->  PostgreSQL
```
All running inside GitHub Codespaces, with PostgreSQL in a Docker container.

## Tech Stack
Python · Pandas · PostgreSQL · Docker · Apache Airflow · psycopg2 · Git

## Dataset
NYC TLC Yellow Taxi Trip Records (Parquet) — 2.96M rows/month, 19 columns.
Source: NYC Taxi & Limousine Commission public data.

## Pipeline Steps
1. **Extract** (`explore_data.py`) — ingest and profile raw Parquet data
2. **Transform** (`transform_data.py`) — clean nulls, remove invalid rows, engineer features
   - 2.96M -> 2.84M rows (4.2% removed)
   - Derived columns: trip_duration_min, pickup_hour, pickup_day_of_week
3. **Load** (`load_to_postgres.py`) — bulk-load into PostgreSQL using psycopg2 COPY
   - Chunked loading (200k rows/batch) for memory efficiency
4. **Orchestrate** (`taxi_etl_dag.py`) — Apache Airflow DAG runs all steps in order, scheduled daily

## Key Results
- Total rows loaded: 2,838,928
- Average fare: $18.52
- Peak demand: 3–7 PM (evening rush hour)
- Busiest day: Wednesday · Quietest: Sunday

## Engineering Challenges Solved
- **Memory constraints** — loading 2.84M rows exceeded available RAM; solved with chunked batch loading via PostgreSQL COPY
- **Dependency conflict** — pandas 3.0 and Airflow's SQLAlchemy 1.4 were incompatible for `to_sql`; resolved by loading through a direct psycopg2 connection
- **Orchestration setup** — configured Airflow in Codespaces (proxy fix, port forwarding) and debugged task failures via Airflow logs

## How to Run
```bash
# 1. Start PostgreSQL
docker run --name taxi-postgres -e POSTGRES_PASSWORD=taxi123 \
  -e POSTGRES_DB=taxidb -p 5432:5432 -d postgres:16

# 2. Run the pipeline manually
python3 scripts/explore_data.py
python3 scripts/transform_data.py
python3 scripts/load_to_postgres.py

# 3. Or orchestrate with Airflow
export AIRFLOW_HOME=~/airflow
cp scripts/taxi_etl_dag.py ~/airflow/dags/
airflow standalone
# then trigger 'taxi_etl_pipeline' from the Airflow UI (port 8080)
```

## Files
```
project-1-batch-etl/
├── scripts/
│   ├── explore_data.py       # Extract
│   ├── transform_data.py     # Transform
│   ├── load_to_postgres.py   # Load
│   └── taxi_etl_dag.py       # Airflow DAG
├── screenshots/              # Airflow graph, results
├── data/                     # (gitignored — not committed)
└── README.md
```

## Status
Complete — full ETL pipeline orchestrated with Airflow, all tasks passing.