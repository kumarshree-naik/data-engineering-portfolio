from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

PROJECT_DIR = "/workspaces/data-engineering-portfolio/project-3-api-pipeline"

default_args = {
    "owner": "kumarshree",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="crypto_price_pipeline",
    default_args=default_args,
    description="Fetch, validate, and store crypto prices on a schedule",
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/5 * * * *",   # every 5 minutes
    catchup=False,
    tags=["api", "crypto", "incremental"],
) as dag:

    fetch_and_load = BashOperator(
        task_id="fetch_validate_load",
        bash_command=f"cd {PROJECT_DIR} && python3 scripts/load_crypto.py",
    )