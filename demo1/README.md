# Demo 1 - Deploying multiple of Microservices with Docker (using legacy way)

## Setup Flask API

```sh
# clone the repo
$ cd demo1/flask-api
$ docker build -t flask:service:latest .
$ docker run -d -p 4001:5001 --name flask_app

#Post this - check the service on localhost:4001
```

## Setup Redis Container

```sh
$ docker rm -f $(docker ps -a -q) #remove all existing container
$ docker pull redis
# Run the redis container
$ docker run -d -p 6379:6379 --name redis redis
```

## Now link Celery and Flask API w/ Redis Container

```sh
# Run flask api and link redis container with it
$ docker run -d -p 4001:5001 --name flask_app --link redis:redis flask_service

# Build Celery Service Image and Run container
$ docker build -t celery_service .
$ docker run -d --name celery_app --link redis:redis celery_service
# Check the API on localhost:4001
# Hit following end point with POST request and send payload 
# URL - localhost:4001/download
# payload = {"url": "image_url_to_be_downloaded"}
```
