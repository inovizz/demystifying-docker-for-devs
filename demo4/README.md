# Demo4

## Changes from previous demo

* docker-compose is changed with more attributes
* New Attribues are:
    - deploy
    - env variables
    - use of .env file
    - mapping volume to current dir

## How to run demo

```sh
$ cd demo4
$ docker-compose up -d
```

## Run with overriding the compose file

```sh
$ docker-compose -f docker-compose.yml -f docker-compose-prod.yml up -d
```
