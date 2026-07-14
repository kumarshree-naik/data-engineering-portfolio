# Project Tracker — Progress

Live status of all projects in this data engineering portfolio.

**Overall progress: 2 of 4 projects complete (50%)**

| # | Project | Key Tools | Status | Complete |
|---|---------|-----------|--------|----------|
| 1 | Batch ETL Pipeline (NYC Taxi) | Airflow, PostgreSQL, Docker | ✅ Done | 100% |
| 2 | Big Data Processing | PySpark, BigQuery | ✅ Done | 100% |
| 3 | Scheduled API Pipeline | Airflow, API, data quality | 🚧 Planned | 0% |
| 4 | Analytics Warehouse | dbt, Snowflake | 🚧 Planned | 0% |

---

## Project 1: Batch ETL Pipeline — ✅ 100%
**Stack:** Python · Airflow · PostgreSQL · Docker · psycopg2

- [x] Environment setup (GitHub, Codespaces, tools)
- [x] Extract — ingest & profile raw Parquet (2.96M rows)
- [x] Transform — clean nulls, remove invalid rows, feature-engineer (2.84M rows)
- [x] Load — batch-load into PostgreSQL via psycopg2 COPY
- [x] Orchestrate — Airflow DAG running all steps in order
- [x] Documented (README) & pushed to GitHub

---

## Project 2: Big Data Processing — ✅ 100%
**Stack:** PySpark · BigQuery · Google Colab

- [x] PySpark setup in Colab (Spark 4.0)
- [x] Load 3 months of data (9.5M rows)
- [x] Clean & feature-engineer at scale (8.5M rows)
- [x] Distributed aggregations (hour, day, distance)
- [x] Load results into BigQuery
- [x] Verify with SQL in BigQuery console
- [x] Documented (README) & pushed to GitHub

---

## Project 3: Scheduled API Pipeline — 🚧 0% (Planned)
**Stack:** Python · Airflow · PostgreSQL · Power BI

- [ ] Connect to a public API (weather / crypto)
- [ ] Ingest data on a schedule
- [ ] Incremental loading (dedupe, no duplicates)
- [ ] Data-quality checks (nulls, ranges, validation)
- [ ] Dashboard on the collected data
- [ ] Document & push to GitHub

*Goal: demonstrate scheduling, incremental loads, and data validation.*

---

## Project 4: Analytics Warehouse — 🚧 0% (Planned)
**Stack:** dbt · Snowflake · Power BI

- [ ] Load raw data into Snowflake
- [ ] Build dbt staging models
- [ ] Build star schema (fact + dimension tables)
- [ ] Add dbt tests & documentation
- [ ] Dashboard on the modeled warehouse
- [ ] Document & push to GitHub

*Goal: demonstrate data modeling, dbt, and cloud warehousing with Snowflake.*

---

*Legend: ✅ Complete · 🚧 In progress / planned · [x] done · [ ] pending*