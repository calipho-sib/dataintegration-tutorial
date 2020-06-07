### Docker Basics


#### Docker installation
A comprehensive resource on docker is the official documentation: https://docs.docker.com/
Installation: https://docs.docker.com/get-docker/


#### Docker Host & Daemon
Docker host is the physical machine where docker daemon is running. Docker daemon is the underlying operating system service which sits between the operating system and the container space.
It facilitates the containers to operate on docker host's resources such as processor, disk and network interfaces. 

 
(https://docs.docker.com/engine/images/architecture.svg)

###### Start docker daemon
Docker daemon starts up in the system boot up. It can be started in multiple different ways depending on the way it is installed.

On Linux:
If docker is installed and made a systemctl service:
```
service docker start | restart | stop
``` 

You can check if the docker service is running as follows on Linux:

```
service docker status
```

On MAC and Windows:


###### Docker CLI

Docker CLI is the command line interface to use the docker service. You can run it as;

```
docker
```

List the images:

```
docker images
```

List the running containers:
```
docker ps
```

To test the installation, we can pull a docker image from docker hub and run it;

```
docker pull hello-world
docker run hello-world
```


#### Dockerfile and Docker images

Docker file represents the configuration of a docker image. Docker image is the blob, which eventually be executed as a container. Docker file starts with the base image on which the containers should be built.
Docker file documentation can be found here: https://docs.docker.com/engine/reference/builder/. Example docker file can be found below;

```
FROM python:alpine3.7
RUN pip install requests
COPY . /app
WORKDIR /app
RUN mkdir  /data
```


#### Building a docker container

Once the docker file is created it had to be build and tagged. To build the image run the following command in the directory with the docker file.
For example, to build the python component in this tutorial, cd to directory /components/python

```
docker build -t sibdays.python .
```

If successful, it should build the docker image and tag it as *sibdays.tutorial.python*. It is possible to list all the docker images identified by the docker service.

```
docker images
``` 

We can build a docker image which encompasses the python programs in /resources/python/ using the docker file in /resources/python/.

```
docker build -t sibdays.python .
docker run sibdays.python
``` 

To delete an image;
```
docker rmi <imageid>
```

#### Running the docker container

Docker container can be run in multiple ways depending on the use case.

Via shell (For most of the images):
You can invoke a command in the image via */bin/sh*. In a way it is similar to logging into the shell in the image and running a command there.

We can run a *ls* command  as follows;

```
docker run sibdays.python ls
```

We can run a python script in the command as follows;
```
docker run sibdays.python /bin/sh -c 'python simple.py'
```

With CMD:
In the docker file, it is possible to add a CMD command for the image, which becomes the command executed;

```
docker run sibdays.python
```

With an entry point:
If a entry point is mentioned as follows, it would become the default command to be executed as well.

```
ENTRYPOINT ["python" "simple.py"]
```

To check the running docker containers;

```
docker ps
```
This will log the existing containers, which can be stopped/removed by;

```
docker stop <containerid>
```

There can be various use cases with docker run, for example passing paramters, environment variables and exposing ports to the docker host. For more details refer to the documentations:
https://docs.docker.com/engine/reference/run/

###### Unix socket and TCP mode
Docker daemon can be started in two main modes. It can either expose a unix socket usually created in ***/var/run/docker.sock***. All the communication with the docker daemon is done via this.
Also it can be started with an exposed TCP socket. This is important when the docker service has to be accessible remotely. More info: https://docs.docker.com/engine/reference/commandline/dockerd/ 
One way to start the docker service in this mode is to create a file called /etc/docker/deamon.json and add following;
```
{
  	"debug": true,
	"hosts": [
		"tcp://0.0.0.0:2375",
		"unix:///var/run/docker.sock"
	]
}
```

Then restart the docker service:
```
sudo systemctl daemon-reload
sudo service docker restart
```

#### Docker registry

Docker registry is a registry which maintains docker images. Docker hub is a centrally maintained registry of docker images. This is the default registry, where docker daemon looks for images.
For example, it is possible to pull an image called *hello-world* from the hub.

```
docker pull hello-world
``` 
In a distributed deployment with multiple machines, it would require to deploy a registry where all the images are published. Since in this workshop we deploy our workflows on a single docker host, we do not need to have a registry.

## Docker compose

Docker compose is a high level composition system on docker, where multiple containers can be composed and execute as a single setup. A simple example of a docker compose can be found in the docker docs.

### Install docker-compose

It can simply be installed by downloading the release with curl.

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

```

We will use docker-compose in the other sessions.

## Docker swarm

Standalone containers are useful in different scenarios and use cases. But when a system gets complicated and contains multiple containers it could get complicated to handle. Container orchestration is a 
concept, which is introduced to solve such complex container settings. While it has multiple uses in different scenarios, few important reasons to use it include, automatic handling of containers, automatic scaling
of container and load balancing. Docker swarm is such a container orchestration system. It handles the mentioned underlying complexity, so that containers can be easily deployed in a orchestrated manner,
