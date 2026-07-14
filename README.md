# Data Engineering Portfolio

## Kumarshree Naik — Data Engineer

M.Tech in Computer Science & Engineering, NIT Rourkela · GATE (CS) 2023 Qualified

📍 Odisha, India
📧 linkannaik40@gmail.com · 💻 [GitHub](https://github.com/kumarshree-naik)

---

## About Me

I build data pipelines — the systems that move raw data from source to a clean,
queryable, analysis-ready state. Coming from a Computer Science background
(M.Tech, NIT Rourkela), I focus on writing pipelines that actually run in
production-like conditions, not just tutorials.

My approach is to build end-to-end on real datasets with industry-standard tools,
and to solve the real engineering problems that come up along the way —
memory limits, dependency conflicts, distributed-processing quirks — rather than
avoiding them. Each project below documents both what I built and the technical
decisions and trade-offs behind it.

**What I work with:** designing ETL/ELT pipelines, orchestrating workflows with
Airflow, distributed processing with PySpark, loading and modeling data in
warehouses (PostgreSQL, BigQuery), and validating data quality along the way.

---

## Technical Skills

| Category | Tools |
|----------|-------|
| **Languages** | Python, SQL, C++ |
| **Orchestration** | Apache Airflow |
| **Big Data** | PySpark (Apache Spark) |
| **Databases / Warehouse** | PostgreSQL, BigQuery |
| **Transformation** | Pandas, NumPy |
| **Infrastructure** | Docker, Git/GitHub, GitHub Codespaces |
| **BI / Visualization** | Power BI, Tableau, Excel |
| **Concepts** | ETL vs ELT, distributed processing, lazy evaluation, data modeling, batch pipelines |

---

## Completed Projects

### 1. Batch ETL Pipeline — NYC Taxi Data
**[View Project →](./project-1-batch-etl)** · `Python` `Airflow` `PostgreSQL` `Docker`

An end-to-end batch ETL pipeline orchestrated with Apache Airflow, processing
~2.96M NYC Yellow Taxi trip records.

- **Extract** raw Parquet → **Transform** (clean, filter, feature-engineer)
  → **Load** into PostgreSQL → **Orchestrate** with an Airflow DAG (extract » transform » load)
- Cleaned 2.96M → 2.84M rows (4.2% removed); engineered trip duration, pickup hour, day of week
- Bulk-loaded via psycopg2 COPY with chunked batching for memory efficiency
- **Engineering challenges solved:** a pandas/SQLAlchemy version conflict, and
  memory constraints on bulk load (solved with chunked COPY)

*Why these choices:* Airflow to turn scripts into a scheduled, monitored pipeline;
PostgreSQL as a queryable destination; Docker to run the database cleanly without
local installs.

---

### 2. Big Data Processing — PySpark + BigQuery
**[View Project →](./project-2-pyspark)** · `PySpark` `BigQuery` `Google Colab`

Distributed processing of ~9.5M NYC taxi records with PySpark, with results
loaded into BigQuery — demonstrating the "Spark processes → warehouse stores" pattern.

- Loaded 3 months of data (9.5M rows), cleaned and feature-engineered at scale (8.5M rows)
- Ran distributed groupBy aggregations (by hour, day, distance bucket) surfacing real insights
- Loaded the aggregated summary into BigQuery and queried it with SQL
- **Engineering note:** resolved a Spark 4.0 timestamp casting issue using unix_timestamp()

*Why these choices:* PySpark to demonstrate distributed processing that scales
beyond a single machine; BigQuery as the cloud warehouse for SQL analytics.
*Honest scope:* at ~8.5M rows the data is moderate — Spark here demonstrates
techniques that scale unchanged to billions of rows.

---

## Repository Structure
```
data-engineering-portfolio/
├── project-1-batch-etl/       # Airflow-orchestrated ETL pipeline  (complete)
├── project-2-pyspark/         # PySpark → BigQuery big-data processing (complete)
├── project-3-api-pipeline/    # Scheduled API pipeline (planned)
├── project-4-dbt-warehouse/   # dbt + Snowflake analytics warehouse (planned)
├── PROGRESS.md                # Full project tracker with status
└── README.md                  # You are here
```

---

## Education & Credentials
- **M.Tech, Computer Science & Engineering** — NIT Rourkela (2023–2025)
- **B.Tech, Information Technology** (2018–2022)
- **GATE (CS) 2023** — Qualified
- **Certifications:** Excel, SQL, Python

---

*Portfolio is actively being built — see [PROGRESS.md](./PROGRESS.md) for live status of all projects.*