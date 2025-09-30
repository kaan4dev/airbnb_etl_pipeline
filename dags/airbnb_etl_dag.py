from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.transform import transform_airbnb_data


default_args = {
    "owner": "data_platform",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="airbnb_etl_pipeline",
    description="Airbnb ETL pipeline orchestrated by Airflow",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["airbnb", "etl"],
) as dag:

    transform = PythonOperator(
        task_id="transform_airbnb_data",
        python_callable=transform_airbnb_data,
    )

    transform
