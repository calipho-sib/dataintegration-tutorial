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

**Note that in the node program, mongo db URL has to be changed according to your IP.**
**Note that in the python program, Loader API URL has to be changed according to your IP.**

Check if the images are created properly with;
```
docker images
```

### Docker operator tasks

Docker operators access the docker host API/service via a TCP connection. Therefore, inorder to properly set the TCP URL, replace the IP of the docker host with the correct one.

```
docker_url="tcp://*.*.*.*:2375",
``` 

Also make sure to modify the path of the volume, as per your repository direction.
```
volumes=['/work/dataintegration-tutorial/sessions/s3.dataintegration/data:/data']
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
Create folders called *data* and *log* in the *s3.dataintegration* folder. This mounts a volume on docker host to the docker container created by the docker operator. 
Go to the airflow admin and start the ETL1 DAG manually. Monitor its status via graph view and logs. If no errors and if the dag executed properly, there will be an output file in *data* folder.

This output file will be read by the node process and written to the mongodb database.

#### Check mongo collections

In order to check if the data is inserted properly to the database, we can log into mongo db as follows;

```
mongo --username testuser --password testpassword --authenticationDatabase ensembl-transformed --host localhost --port 27017
```

To check the data;
```
use ensembl-transformed
db.ensembl.find({})
```

If the loading is done properly, you will see data.

### Synchronous pipeline

In this workflow, we do not rely on writing to the docker host, but we run both processes in parallel and python program calls an API running on the node.js process. While there are multiple options to do this, an easy way is to run node process as a service.
We can do this by adding following service block to the docker-compose config file.

```
loader:
    image: 'sibdays.node'
    ports:
      - "3000:3000"
    command: ./start-api
```

Go to the airflow admin and start the ETL2 DAG manually. Monitor its status via graph view and logs.

