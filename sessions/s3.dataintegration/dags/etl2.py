from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'airflow',
    'description'           : 'Use of the DockerOperator',
    'depend_on_past'        : False,
    'start_date'            : datetime(2020, 6, 6),
    'email_on_failure'      : False,
    'email_on_retry'        : False,
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=5)
}

with DAG('etl2', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    t1 = BashOperator(
        task_id='print_current_date',
        bash_command='date'
    )


    t2 = DockerOperator(
        task_id='extract1',
        image='sibdays.python',
        api_version='auto',
        auto_remove=True,
        command="python extract.py 1 10",
        docker_url="tcp://172.31.29.142:2375",
        network_mode="bridge",
        environment={"MODE": "FILE"},
        volumes=['/work/sibdays/dataintegration-tutorial/sessions/s3.dataintegration/data:/data']
    )

    t3 = DockerOperator(
        task_id='extract2',
        image='sibdays.python',
        api_version='auto',
        auto_remove=True,
        command="python extract.py 11 20",
        docker_url="tcp://172.31.29.142:2375",            
        network_mode="bridge",
        environment={"MODE": "FILE"},
        volumes=['/work/sibdays/dataintegration-tutorial/sessions/s3.dataintegration/data:/data']
    )

    t4 = DockerOperator(
        task_id='transform-load1',
        image='sibdays.node',
        api_version='auto',
        auto_remove=True,
        command="node transform-load.js /data/ensembl1-10.json",
        docker_url="tcp://172.31.29.142:2375",
        network_mode="bridge",
        environment={"MODE": "FILE"},
        volumes=['/work/sibdays/dataintegration-tutorial/sessions/s3.dataintegration/data:/data']
    )

    t5 = DockerOperator(
        task_id='transform-load2',
        image='sibdays.node',
        api_version='auto',
        auto_remove=True,
        command="node transform-load.js /data/ensembl11-20.json",
        docker_url="tcp://172.31.29.142:2375",
        network_mode="bridge",
        environment={"MODE": "FILE"},
        volumes=['/work/sibdays/dataintegration-tutorial/sessions/s3.dataintegration/data:/data']
    )

    t6 = BashOperator(
        task_id='t2',
        bash_command='date'
    )



    t1  >> t2 >> t4 >> t6
    t1  >> t3 >> t5 >> t6
