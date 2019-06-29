# Demo3

## Changes from previous demo

* docker-compose is changed with more attributes
* New Attribues are:
    - build
    - networks
    - volumes

## How to run demo

```sh
$ $ docker rm -f $(docker ps -a -q)
$ cd demo3
$ docker-compose up -d
```
