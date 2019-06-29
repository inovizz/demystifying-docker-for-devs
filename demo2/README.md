# Demo2

## Changes from previous demo

- Added logging in code
- Changed Dockerfiles to include LOG and FILE paths.
- Added docker-compose

## How to run demo

```sh
$ docker rm -f $(docker ps -a -q)
$ cd demo2
$ cd flask_api
$ docker build -t flask_service .
$ cd ../taskqueue
$ docker build -t celery_service .
$ cd ..
$ docker-compose up -d
```
