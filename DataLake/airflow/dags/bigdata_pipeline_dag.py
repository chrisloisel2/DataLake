from airflow import DAG
from airflow.providers.apache.hive.operators.hive import HiveOperator
# OU utilisez Impyla comme alternative
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

with DAG(
    'hive_example',
    default_args=default_args,
    schedule_interval=None
) as dag:

    hive_op = HiveOperator(
        task_id='hive_query',
        hql='SELECT * FROM your_table LIMIT 10',
        hive_cli_conn_id='hiveserver2_default'
    )
