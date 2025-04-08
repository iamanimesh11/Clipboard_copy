from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2
import logging

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def check_etl_health():
    logging.info("Starting ETL health check...")
    
    conn = psycopg2.connect(
        host="your_postgres_host",
        port="your_postgres_port",
        database="your_db_name",
        user="your_user",
        password="your_password"
    )
    cur = conn.cursor()

    tables = {
        'roaddata': 'created_at',
        'trafficdata': 'recorded_at'
    }

    for table, time_col in tables.items():
        cur.execute(f"SELECT MAX({time_col}) FROM {table};")
        latest_time = cur.fetchone()[0]

        cur.execute(f"SELECT COUNT(*) FROM {table};")
        row_count = cur.fetchone()[0]

        logging.info(f"{table} | Latest: {latest_time} | Rows: {row_count}")

        if latest_time is None or (datetime.now() - latest_time) > timedelta(minutes=20):
            logging.warning(f"{table} data might be stale!")

    cur.close()
    conn.close()

with DAG(
    'monitor_etl_health_dag',
    default_args=default_args,
    schedule_interval='*/10 * * * *',
    catchup=False
) as dag:

    monitor_task = PythonOperator(
        task_id='check_etl_status',
        python_callable=check_etl_health
    )

    monitor_task