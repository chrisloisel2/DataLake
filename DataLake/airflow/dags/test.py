from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"owner": "airflow", "start_date": datetime(2025, 4, 7)}
dag = DAG("hive_quickstart_robust", default_args=default_args, schedule_interval=None)

create_table = BashOperator(
    task_id="create_hive_table_safe",
    bash_command="""
/usr/bin/beeline -u "jdbc:hive2://hive-server:10000" -e "
    CREATE TABLE IF NOT EXISTS robust_test (
        id INT,
        value STRING,
        load_ts TIMESTAMP
    )
    STORED AS PARQUET
    "
""",
    dag=dag
)
