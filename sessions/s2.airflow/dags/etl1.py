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

with DAG('docker_dag', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    t1 = BashOperator(
        task_id='print_current_date',
        bash_command='date'
    )


    t2 = DockerOperator(
        task_id='docker_command',
        image='sibdays.python',
        api_version='auto',
        auto_remove=True,
        command="python extract.py 1 10",
        docker_url="tcp://172.31.17.235:2375",
        network_mode="bridge",
        volumes=['/work/dataintegration-tutorial/sessions/s2.airflow/data:/data']
    )

    t3 = BashOperator(
        task_id='t2',
        bash_command='date'
    )



    t1  >> t2 >> t3