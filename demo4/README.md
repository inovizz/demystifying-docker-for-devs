# Demo4

## Changes from previous demo

* docker-compose is changed with more attributes
* New Attribues are:
  * deploy
  * env variables
  * use of .env file`
  * mapping volume to current dir instead of a user specified docker volume

## How to run demo4?

```sh
$ docker rm -f $(docker ps -a -q)
$ cd demo4
$ docker-compose up -d
```

## Run with overriding the compose file

```sh
$ docker-compose -f docker-compose.yml -f docker-compose-prod.yml up -d
```

## Try out deploy key given in Docker-Compose file

Visit this [tutorial](https://docs.docker.com/get-started/part3/) to try out how deploy key is being used.
