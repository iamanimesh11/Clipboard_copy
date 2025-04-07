from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.road_producer_etl import create_road_topic, produce_road_data

with DAG(
    dag_id="road_kafka_producer_dag",
    start_date=datetime(2025, 4, 7),
    schedule_interval="@hourly",  # or your preferred schedule
    catchup=False,
    tags=["kafka", "producer", "roads"],
    default_args={"retries": 2, "retry_delay": timedelta(minutes=2)}
) as dag:

    create_topic = PythonOperator(
        task_id="create_road_topic",
        python_callable=create_road_topic
    )

    send_road_data = PythonOperator(
        task_id="produce_road_data",
        python_callable=produce_road_data
    )

    create_topic >> send_road_data