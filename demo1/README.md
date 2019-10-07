# Demo 1 - Connecting multiple Microservices

## Setup Flask API Container

```sh
# clone the repo
$ cd demo1/flask-api
$ docker build -t flask_service:latest .
$ docker run -d -p 4001:5001 --name flask_app flask_service
# Post this - check the service on localhost:4001
# The output will show that redis connection is broken and you will see following error message -
Visits: cannot connect to Redis, counter disabled
# So in next step lets setup redis container and try and link it with flask_api container
```

## Setup Redis Container

```sh
$ docker rm -f $(docker ps -a -q) #remove all existing container
$ docker pull redis
# Run the redis container
$ docker run -d -p 6379:6379 --name redis redis
```

## Link Flask API container w/ Redis Container

```sh
# Run flask api and link redis container with it
$ docker run -d -p 4001:5001 --name flask_app --link redis:redis flask_service
```

## Link Celery service container w/ Redis Container

```sh
# Build Celery Service Image and Run container
$ cd ../taskqueue
$ docker build -t celery_service .
$ docker run -d --name celery_app --link redis:redis celery_service
# To validation API Endpoints try hitting following end point with POST request and send payload
# URL - localhost:4001/download
# payload = {"url": "image_url_to_be_downloaded", "file_name": "file_name"}
```

## Reference for Topics covered till Demo 1

* 
* 
* 
* 
* 
* 
