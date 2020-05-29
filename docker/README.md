### Docker Basics


#### Docker installtion
https://docs.docker.com/get-docker/


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

You can check if the docker service is running as follows:

```
service docker status
```

###### Unix socket and TCP mode
Docker daemon can be started in two main modes. It can either expose a unix socket usually created in ***/var/run/docker.sock***. All the communication with the docker daemon is done via this.
Also it can be started with an exposed TCP socket. 
```
service docker status
```


#### Dockerfile

Docker file represents the configuration of a docker container.  

```
Give examples
```


#### Building a docker container

Once the docker file is created it had to be build and tagged.

```
docker build -t .
```


#### Running the docker container

## Docker compose

## Docker swarm

