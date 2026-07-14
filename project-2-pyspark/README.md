# Project 2: Big Data Processing with PySpark + BigQuery

Distributed processing of NYC taxi data using PySpark, with results loaded into BigQuery — demonstrating the "Spark processes → warehouse stores" pattern.

## Overview
Processed ~9.5M NYC Yellow Taxi trip records (3 months) with PySpark, then loaded the aggregated results into BigQuery for SQL analytics.

## Tech Stack
PySpark (Apache Spark 4.0) · BigQuery · Google Colab · Python · Parquet

## Dataset
NYC TLC Yellow Taxi Trip Records — Jan–Mar 2024 (Parquet)
- 9,554,778 raw rows → 8,479,468 after cleaning
- 19 columns

## Pipeline
1. **Load** — read 3 months of Parquet into a Spark DataFrame (wildcard)
2. **Clean** — filter invalid rows (zero fares, zero distance, bad dates) at scale
3. **Feature Engineering** — trip_duration_min, pickup_hour, pickup_day
4. **Aggregate** — distributed groupBy analytics (by hour, day, distance bucket)
5. **Load to Warehouse** — write hourly summary into BigQuery (dataset: taxi_analytics)
6. **Query** — SQL analytics on the results in BigQuery

## Key Insights
- Peak demand: 3–6 PM (afternoon/evening rush)
- Highest average fare at 5 AM (~$27.66) — likely early airport runs
- 57% of trips under 2 miles (short city hops)
- Fares & tips scale with distance (0–2 mi ~$10 → 10+ mi ~$65)
- Busiest day: Thursday · Quietest: Monday

## Spark Concepts Demonstrated
- Distributed processing (partitioned, parallel)
- Lazy evaluation (transformations vs actions)
- Spark → small-result handoff (aggregates to Pandas → warehouse)

## Engineering Notes
- Resolved a Spark 4.0 timestamp issue (TIMESTAMP_NTZ cast) using unix_timestamp()
- Ran entirely in Google Colab (cloud compute) — no local cluster

## Note on Scale
Dataset (~155MB, 8.5M rows) is moderate; SQL/Pandas could also handle it. PySpark demonstrates distributed techniques that scale unchanged to billions of rows.

## Status
✅ Complete — Spark processing + BigQuery warehouse load, verified with SQL.