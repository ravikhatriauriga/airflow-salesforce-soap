from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from salesforce_pdf_logic import fetch_and_send_pdf


default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'salesforce_pdf_to_soap_api',
    default_args=default_args,
    schedule_interval='@daily',  # Adjust the interval as needed
    catchup=False,
)

fetch_and_send_task = PythonOperator(
    task_id='fetch_and_send_pdf',
    python_callable=fetch_and_send_pdf,
    dag=dag,
)

fetch_and_send_task
