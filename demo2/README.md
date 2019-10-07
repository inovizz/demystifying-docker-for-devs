# Demo2

In previous demo we talked about how to spawn a docker container and then how to run multiple docker containers and learn how to link them. However, there is a lot of typng you may have to do and make sure to follow certain to steps to start all the containers. With this demo, we'll see how docker-compose makes our life easier, which means we don't need to worry much about linking containers and starting them one by one. That magic happens from docker-compose.

## Changes from previous demo

Coming to changes we have in this demo from previous one, firstly we have simply copied whole code from demo1 to demo2 but along with that we have done following changes in the code -

- Added logging in code (flask_api and celery service)
- Changed Dockerfiles to include LOG and FILE paths
- Added docker-compose file and define all services

## Now how to run demo?

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
```
