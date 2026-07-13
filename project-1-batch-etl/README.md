Project 1: Batch ETL Pipeline (NYC Taxi Data)

An end-to-end batch ETL pipeline that ingests NYC Yellow Taxi trip data,
cleans and transforms it, loads it into PostgreSQL, and orchestrates the
whole workflow with Apache Airflow.

Architecture

Airflow DAG  ->  extract  ->  transform  ->  load  ->  PostgreSQL

All running inside GitHub Codespaces, with PostgreSQL in a Docker container.

Tech Stack

Python · Pandas · PostgreSQL · Docker · Apache Airflow · psycopg2 · Git

Dataset

NYC TLC Yellow Taxi Trip Records (Parquet) — 2.96M rows/month, 19 columns.
Source: NYC Taxi & Limousine Commission public data.

Pipeline Steps


Extract (explore_data.py) — ingest and profile raw Parquet data
Transform (transform_data.py) — clean nulls, remove invalid rows, engineer features

2.96M -> 2.84M rows (4.2% removed)
Derived columns: trip_duration_min, pickup_hour, pickup_day_of_week



Load (load_to_postgres.py) — bulk-load into PostgreSQL using psycopg2 COPY

Chunked loading (200k rows/batch) for memory efficiency



Orchestrate (taxi_etl_dag.py) — Apache Airflow DAG runs all steps in order, scheduled daily


Key Results


Total rows loaded: 2,838,928
Average fare: $18.52
Peak demand: 3–7 PM (evening rush hour)
Busiest day: Wednesday · Quietest: Sunday


Engineering Challenges Solved


Memory constraints — loading 2.84M rows exceeded available RAM; solved with
chunked batch loading via PostgreSQL COPY
Dependency conflict — pandas 3.0 and Airflow's SQLAlchemy 1.4 were incompatible
for to_sql; resolved by loading through a direct psycopg2 connection
Orchestration setup — configured Airflow in Codespaces (proxy fix, port
forwarding) and debugged task failures via Airflow logs


How to Run

bash# 1. Start PostgreSQL
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

Files

project-1-batch-etl/
├── scripts/
│   ├── explore_data.py       # Extract
│   ├── transform_data.py     # Transform
│   ├── load_to_postgres.py   # Load
│   └── taxi_etl_dag.py       # Airflow DAG
├── screenshots/              # Airflow graph, results
├── data/                     # (gitignored — not committed)
└── README.md

Status

Complete — full ETL pipeline orchestrated with Airflow, all tasks passing.

---COPY ABOVE THIS LINE---


PART 2 — PROGRESS.md Day 5 Entry

Where it goes: add this under the Day 4 entry in your root PROGRESS.md.

---COPY BELOW THIS LINE---

Day 5 — Orchestrate (Apache Airflow)


Installed Apache Airflow 2.9.3 and ran it in standalone mode
Wrote taxi_etl_dag.py — a DAG with 3 tasks: extract >> transform >> load
Configured Airflow in Codespaces (proxy fix, port forwarding for the web UI)
Debugged and solved real failures:

Port collisions from lingering processes (force-killed and cleaned PID files)
pandas 3.0 vs SQLAlchemy 1.4 conflict (rewrote load to use psycopg2 COPY)
Memory limit on bulk load (chunked COPY at 200k rows/batch)



Result: full pipeline runs end-to-end in Airflow, all 3 tasks green
Project 1 COMPLETE — a working, orchestrated batch ETL pipeline


---COPY ABOVE THIS LINE---


PART 3 — Commit Commands

Run these in a terminal (not the one running Airflow):

bashcd /workspaces/data-engineering-portfolio
git add .
git commit -m "Day 5: Project 1 complete - Airflow orchestration + final README"
git push


PART 4 — Add the Airflow screenshot to your repo (optional but recommended)


Take a screenshot of the green Airflow Graph (all 3 tasks dark green).
In the Codespace file explorer, create folder: project-1-batch-etl/screenshots/
Drag the screenshot file into that folder (or upload it).
Commit again:


bashgit add .
git commit -m "Add Airflow pipeline success screenshot"
git push


Project 1 — Done. What you built:


A real ETL pipeline: Extract -> Transform -> Load, orchestrated by Airflow
Processed ~3M rows, cleaned to 2.84M, loaded into PostgreSQL
Solved genuine engineering problems: memory limits, dependency conflicts, orchestration setup


Interview one-liners


"I built an Airflow-orchestrated batch ETL pipeline processing ~3M NYC taxi trips."
"I hit a pandas/SQLAlchemy version conflict and re-engineered the load to use psycopg2 COPY."
"I solved memory limits with chunked bulk loading — a technique that scales to any data size."
"The pipeline runs extract, transform, and load as scheduled Airflow tasks with retries."



Next: Project 2 — Big Data Processing with PySpark (Colab + BigQuery).