## Workflow Management with Apache Airflow

Apache airflow (https://airflow.apache.org/) is a workflow management framework. It is an open source apache project with a strong community.

### Airflow Basics

Airflow has multiple different components.

1. Scheduler

Scheduler is a core of the airflow engine, which handles the scheduling of the processes.

2. Web server

Web server hosts the admin interface of airflow, which has a comprehensive control panel for DAGs.

3. Database

Airflow maintains a database to store operational data. It is possible to configure different databases, such as sqlite, postgres or any other.


#### Defining airflow workflows as DAGs

Directed Acyclic Graph (https://airflow.apache.org/docs/stable/concepts.html) is the fundamental abstraction of airflow to represent a workflow. Inherent directionality of the definition provides a sequentially of sub processes in the DAG.
An airflow DAG is written in python, using the airflow API. Python interface for DAG looks like below;

```
with DAG('docker_dag', default_args=default_args, schedule_interval=None, catchup=False) as dag:
        t1 = BashOperator(
                task_id='print_current_date',
                bash_command='date'
        )
    
        t2 = SimpleHttpOperator(
                task_id='get_templates',
                method='GET',
                endpoint='/v3/templates',
                http_conn_id = 'conn_id',
                trigger_rule="all_done",
        )

        t3 = BashOperator(
                task_id='t2',
                bash_command='date'
        )

        t1  >> t2 >> t3

```

#### Schedule
*schedule_interval* is the parameter, which controls the execution schedule of a DAG. According to the schedule_interval, DAG is scheduled for execution automatically. If the *schedule_interval* is null, DAG has to be started manually via the admin interface or CLI.



### Airflow Installation 

Airflow installation can be done in different ways. As airflow is a python package, it can be installed in standard python installation mechanisms such as pip or pipenv.
More info: https://airflow.apache.org/docs/stable/installation.html
With pip:
```
pip install apache-airflow
```

#### Airflow configuration & Start

Airflow is a configurable system with various different options to handle different parts of the system. Configuration has to be set in the way we want to start airflow.
Once the airflow configuration is set, scheduler and web server has to be started. If the configuration set to a non-file based database such as postgres or mysql, database server has to be started.


### Airflow with Docker Compose

A rather easy approach is to use docker compose to start these components all together. We use the docker compose file *airflow-docker-compose.yml* provided in this d


```
docker-compose up -f docker-compose-ariflow.yml up --build
```

You can start it with -d switch, so that it will start in the background. Otherwise you will see the logs from the compose startup, where you can see the status. If no error, you can check the airflow setup as;

```
docker-compose ps or docker ps
```

You can see if the airflow related processes are properly started.

#### Airflow admin interface

Once airflow started properly, you can go to the airflow web interface, through which you can manage airflow workflows.

### Simple DAG example


