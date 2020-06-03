## Workflow Management with Apache Airflow



### Airflow Basics

```
Give an example
```

### Airflow Installation 

Explain what these tests test and why

```
Give an example
```

### Airflow with Docker Compose

Airflow has multiple different components. It should at least comprise of following components.

1. Scheduler
2. Web server
3. Database

These components has to be started and managed separately to start airflow. A rather easy approach is to use docker compose to start these components all together.
We use the docker compose file provided in the repository to start it. You can start it as;


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

### First example with Airflow
