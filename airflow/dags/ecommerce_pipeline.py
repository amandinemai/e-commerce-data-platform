from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

# Default arguments applied to all tasks
default_args = {
    "owner": "data-team",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

DBT_DIR = "/opt/airflow/dbt"
DBT_PROFILES_DIR = "/opt/airflow/dbt"
DBT_TARGET = "docker"

with DAG(
    dag_id="ecommerce_pipeline",
    description="E-commerce data pipeline: seed → staging → marts → tests",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["ecommerce", "dbt", "bigquery"],
) as dag:

    # -------------------------
    # Start
    # -------------------------
    start = EmptyOperator(task_id="start")

    # -------------------------
    # Step 1 — Load seeds
    # -------------------------
    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=f"cd {DBT_DIR} && dbt seed --profiles-dir {DBT_PROFILES_DIR} --target {DBT_TARGET}",
    )

    # -------------------------
    # Step 2 — Run staging models
    # -------------------------
    dbt_run_staging = BashOperator(
        task_id="dbt_run_staging",
        bash_command=f"cd {DBT_DIR} && dbt run --select staging --profiles-dir {DBT_PROFILES_DIR} --target {DBT_TARGET}",
    )

    # -------------------------
    # Step 3 — Run marts models
    # -------------------------
    dbt_run_marts = BashOperator(
        task_id="dbt_run_marts",
        bash_command=f"cd {DBT_DIR} && dbt run --select marts --profiles-dir {DBT_PROFILES_DIR} --target {DBT_TARGET}",
    )

    # -------------------------
    # Step 4 — Run data quality tests
    # -------------------------
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && dbt test --profiles-dir {DBT_PROFILES_DIR} --target {DBT_TARGET}",
    )

    # -------------------------
    # Step 5 — Generate docs
    # -------------------------
    dbt_docs = BashOperator(
        task_id="dbt_docs_generate",
        bash_command=f"cd {DBT_DIR} && dbt docs generate --profiles-dir {DBT_PROFILES_DIR} --target {DBT_TARGET}",
    )

    # -------------------------
    # End
    # -------------------------
    end = EmptyOperator(task_id="end")

    # -------------------------
    # DAG dependencies
    # -------------------------
    start >> dbt_seed >> dbt_run_staging >> dbt_run_marts >> dbt_test >> dbt_docs >> end