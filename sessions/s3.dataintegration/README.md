## Data Integration Pipeline Patterns

Aim of this session is to build a containerized airflow workflow with the Docker operator. We use two simple processes one written in Python and one written in node.js and define the workflow.

### Build docker images for the processes

Python process:
Change directory to *resources/python* and do;
```
docker build -t sibdays.python .
```

node.js process:
Change directory to *resources/node* and do;
```
docker build -t sibdays.node .
```

Check if the images are created properly with;
```
docker images
```

### Asynchronous I/O based pipelines  

In this workflow, we have the python process (Extract step), which runs and generates an output, which is written to the local disk (On the host). 
Once this process is finished, node.js process  runs, which reads from the output file and do some processing and writes to the db. 

#### Mongodb
In order to setup the destination datasource, as in this case a mongo db instance we add the following service block to the docker-compose file.

```
mongo:
    image: 'mongo'
    environment:
      - MONGO_INITDB_DATABASE=ensembl-transformed
      - MONGO_INITDB_ROOT_USERNAME=testuser
      - MONGO_INITDB_ROOT_PASSWORD=testpassword
    volumes:
      - ./mongo/init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js:ro
    ports:
      - "27017:27017"
```

Note that an init-mongo.js file is added in the *mongo*, which sets up the initial database and username, password pair.

In order to support the local writing to the docker host, we have to mount a volume to the docker container. This can be done via the docker operator definition in the dag file *dags/etl1*.
```
volumes=['/work/dataintegration-tutorial/sessions/s2.airflow/data:/data']
```
Create a folder called *data* in the *s3.dataintegration* folder. This mounts a volume on docker host to the docker container created by the docker operator. 
Go to the airflow admin and start the ETL1 DAG manually. Monitor its status via graph view and logs. If no errors and if the dag executed properly, there will be an output file in *data* folder.

This output file will be read by the node process and written to the mongodb database.

### Synchronous pipeline

In this workflow, we do not rely on writing to the docker host, but we run both processes in parallel and python program calls an API running on the node.js process.


Go to the airflow admin and start the ETL2 DAG manually. Monitor its status via graph view and logs.

