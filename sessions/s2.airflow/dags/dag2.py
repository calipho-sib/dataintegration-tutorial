from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'airflow',
    'description'           : 'Use of the DockerOperator',
    'depend_on_past'        : False,
    'start_date'            : datetime(2018, 1, 3),
    'email_on_failure'      : False,
    'email_on_retry'        : False,
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=5)
}

with DAG('worflow1', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    t1 = BashOperator(
        task_id='print_current_date',
        bash_command='date'
    )

    t2 = BashOperator(
        task_id='sleep_10',
        bash_command='sleep 10'
    )

    t3 = BashOperator(
        task_id='sleep_20',
        bash_command='sleep 20'
    )

    t4 = BashOperator(
        task_id='echo_bye',
        bash_command='echo \'I am Done BYE\''
    )

    t1  >> [t2,t3] >> t4