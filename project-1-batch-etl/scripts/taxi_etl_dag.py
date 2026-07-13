from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Path to your project (adjust if needed)
PROJECT_DIR = "/workspaces/data-engineering-portfolio/project-1-batch-etl"

default_args = {
    "owner": "kumarshree",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="taxi_etl_pipeline",
    default_args=default_args,
    description="Batch ETL pipeline for NYC taxi data",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",   # runs once a day
    catchup=False,
    tags=["etl", "taxi"],
) as dag:

    # Task 1: Extract / explore
    extract = BashOperator(
        task_id="extract",
        bash_command=f"cd {PROJECT_DIR} && python3 scripts/explore_data.py",
    )

    # Task 2: Transform
    transform = BashOperator(
        task_id="transform",
        bash_command=f"cd {PROJECT_DIR} && python3 scripts/transform_data.py",
    )

    # Task 3: Load
    load = BashOperator(
        task_id="load",
        bash_command=f"cd {PROJECT_DIR} && python3 scripts/load_to_postgres.py",
    )

    # Define the order: extract -> transform -> load
    extract >> transform >> load