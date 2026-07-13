# Project 1: Batch ETL Pipeline

## Overview
End-to-end batch ETL pipeline: ingests NYC Yellow Taxi trip data,
cleans and transforms it, loads into PostgreSQL, orchestrated with Apache Airflow.

## Dataset
NYC TLC Yellow Taxi Trip Records (Parquet) — ~2.96M rows/month, 19 columns.

## Tech Stack
Python · Pandas · PostgreSQL · Apache Airflow · Docker

## Status
🚧 In progress — Day 3: transformation complete (2.84M clean rows, 4.2% removed).

## Pipeline Steps
1. Ingest raw Parquet data
2. Clean & transform (nulls, types, invalid rows)
3. Load into PostgreSQL
4. Orchestrate with Airflow DAG