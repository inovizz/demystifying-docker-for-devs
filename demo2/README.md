# Demo2

In previous demo we talked about how to spawn a docker container and then how to run multiple docker containers and learn how to link them. However, there is a lot of typng you may have to do and make sure to follow certain to steps to start all the containers. With this demo, we'll see how docker-compose makes our life easier, which means we don't need to worry much about linking containers and starting them one by one. That magic happens from docker-compose.

## Changes from previous demo

Coming to changes we have in this demo from previous one, firstly we have simply copied whole code from demo1 to demo2 but along with that we have done following changes in the code -

- Added logging in code (flask_api and celery service)
- Changed Dockerfiles to include LOG and FILE paths
- Added docker-compose file and define all services

## Now how to run demo2?

```sh
# first of all remove all previous containers so that there is no conflict w.r.t using same
# container names
$ docker rm -f $(docker ps -a -q)
# once containers removed build the flask_api and celery_service images again
# since we have added code changes w.r.t. logging
$ cd demo2/flask_api
$ docker build -t flask_service .
$ cd ../taskqueue
$ docker build -t celery_service .
$ cd ..
# now run docker-compose and see how a single command spawns all of your containers and does the 
# same job for which we were running 4-5 commands in demo1
$ docker-compose up -d
# Now follow the same steps to test the microservices as mentioned in Demo1
# once test is completed, use below command to remove and stop all containers
$ docker-compose down
```

## Reference for Topics covered post Demo 1

- [Docker Commands](https://docs.docker.com/engine/reference/commandline/docker/)
- [Entrypoint vs CMD](https://www.learnitguide.net/2018/06/dockerfile-cmd-entrypoint-differences.html)
- [ADD vs COPY](https://nickjanetakis.com/blog/docker-tip-2-the-difference-between-copy-and-add-in-a-dockerile)
- [Introduction to Docker Compose](https://docs.docker.com/compose/)
- [Docker file reference](https://docs.docker.com/engine/reference/builder/)
- [Multistage Docker Builds](https://docs.docker.com/develop/develop-images/multistage-build/)
- [Docker Images Best Practices](https://www.youtube.com/watch?v=JofsaZ3H1qM)
