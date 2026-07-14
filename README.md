# Data Engineering Portfolio

## Kumarshree Naik — Data Engineer

M.Tech in Computer Science & Engineering, NIT Rourkela · GATE (CS) 2023 Qualified

📍 Odisha, India
📧 linkannaik40@gmail.com · 💻 [GitHub](https://github.com/kumarshree-naik)

---

## About

I build data pipelines — the systems that move raw data from source to a
clean, queryable, analysis-ready state. This repository is a hands-on
collection of data engineering projects covering batch ETL, big-data
processing, scheduled pipelines, and analytics modeling.

Each project is built end-to-end on real datasets, using industry-standard
tools, with a focus on writing pipelines that actually run — not just
tutorials. Where I hit real engineering problems (memory limits, dependency
conflicts, orchestration issues), I've documented how I solved them.

---

## Tech Stack

| Category | Tools |
|----------|-------|
| **Languages** | Python, SQL, C++ |
| **Orchestration** | Apache Airflow |
| **Databases / Warehouse** | PostgreSQL, BigQuery |
| **Big Data** | PySpark |
| **Transformation** | Pandas, dbt |
| **Infrastructure** | Docker, Git/GitHub, GitHub Codespaces |
| **BI / Visualization** | Power BI, Tableau, Excel |

---

## Projects

### 1. Batch ETL Pipeline — NYC Taxi Data ✅
**[View Project →](./project-1-batch-etl)**

An end-to-end batch ETL pipeline orchestrated with Apache Airflow, processing
~2.96M NYC Yellow Taxi trip records.

- **Extract** raw Parquet data → **Transform** (clean, filter, feature-engineer)
  → **Load** into PostgreSQL → **Orchestrate** with an Airflow DAG
- Cleaned 2.96M → 2.84M rows (4.2% removed); engineered trip duration,
  pickup hour, and day-of-week features
- Bulk-loaded via psycopg2 COPY with chunked batching for memory efficiency
- **Solved:** a pandas/SQLAlchemy version conflict and memory constraints on load

`Python` · `Airflow` · `PostgreSQL` · `Docker` · `psycopg2` · `Pandas`

---

### 2. Big Data Processing — PySpark 🚧
**Status: In progress**

Large-scale processing of taxi data using PySpark, with results loaded into
BigQuery. Demonstrates distributed processing and cloud warehousing.

`PySpark` · `BigQuery` · `Google Colab`

---

### 3. Scheduled API Data Pipeline 🚧
**Status: Planned**

A pipeline that pulls fresh data from a public API on a schedule, with
incremental loading and data-quality checks, feeding a live dashboard.

`Python` · `Airflow` · `PostgreSQL` · `Power BI`

---

### 4. Analytics Warehouse — dbt 🚧
**Status: Planned**

Modern analytics-engineering: raw data transformed into a clean star schema
with dbt, modeled in BigQuery, and visualized in Power BI.

`dbt` · `BigQuery` · `Power BI`

---

## Repository Structure
```
data-engineering-portfolio/
├── project-1-batch-etl/       # Airflow-orchestrated ETL pipeline
├── project-2-pyspark/         # (in progress)
├── project-3-api-pipeline/    # (planned)
├── project-4-dbt-warehouse/   # (planned)
├── PROGRESS.md                # Day-by-day build log
└── README.md                  # You are here
```

---

## Background

- **M.Tech, Computer Science & Engineering** — NIT Rourkela (2023–2025)
- **B.Tech, Information Technology** (2018–2022)
- **GATE (CS) 2023** — Qualified
- **Certifications:** Excel, SQL, Python

---

*This portfolio is actively being built. Follow along in [PROGRESS.md](./PROGRESS.md).*
