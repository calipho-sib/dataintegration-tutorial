## Data Integration Pipeline Patterns

Aim of this session is to build a containerized airflow workflow with the Docker operator. We use two simple processes one written in Python and one written in node.js and define the workflow.

### Build docker images for the processes

Python process:
Change directory to *resources/python* and do;
```
docker build -t sibdays.tutorial.python .
```

node.js process:
Change directory to *resources/node* and do;
```
docker build -t sibdays.tutorial.node .
```

Check if the images are created properly with;
```
docker images
```

### Asynchronous I/O based pipelines  

In this workflow, we have the python process (Extract step), which runs and generates an output, which is written to the local disk (On the host). 
Once this process is finished, node.js process  runs, which reads from the output file and do some processing and writes to the db. 

In order to support the local writing to the docker host, we have to mount a volume to the docker container. This can be set in the docker compose file. 
Go to the airflow admin and start the ETL1 DAG manually. Monitor its status via graph view and logs.

### Synchronous pipeline

In this workflow, we do not rely on writing to the docker host, but we run both processes in parallel and python program calls an API running on the node.js process.

Go to the airflow admin and start the ETL2 DAG manually. Monitor its status via graph view and logs.