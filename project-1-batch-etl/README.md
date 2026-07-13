# Project 1: Batch ETL Pipeline

## Overview
End-to-end batch ETL pipeline: ingests NYC Yellow Taxi trip data,
cleans and transforms it, loads into PostgreSQL, orchestrated with Apache Airflow.

## Dataset
NYC TLC Yellow Taxi Trip Records (Parquet) — ~2.96M rows/month, 19 columns.

## Tech Stack
Python · Pandas · PostgreSQL · Docker · Apache Airflow

## Status
🚧 In progress — Day 4: Load complete. 2.84M clean rows in PostgreSQL, verified with SQL.

## Pipeline Steps
1. **Extract** — ingest raw Parquet data (`explore_data.py`)
2. **Transform** — clean nulls, remove invalid rows, add derived columns (`transform_data.py`)
   - 2.96M → 2.84M rows (4.2% removed)
   - Derived: trip_duration_min, pickup_hour, pickup_day_of_week
3. **Load** — batch-load into PostgreSQL, verify with SQL (`load_to_postgres.py`)
   - Loaded in chunks of 10k for memory efficiency
4. **Orchestrate** — Apache Airflow DAG (upcoming)

## Key Results
- Peak demand: 3–7 PM (evening rush)
- Average fare: $18.52
- Busiest day: Wednesday

## How to Run
```bash
# Start PostgreSQL
docker run --name taxi-postgres -e POSTGRES_PASSWORD=taxi123 \
  -e POSTGRES_DB=taxidb -p 5432:5432 -d postgres:16

# Run the pipeline
python3 scripts/explore_data.py
python3 scripts/transform_data.py
python3 scripts/load_to_postgres.py
```