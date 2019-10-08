# Demo3

## Changes from previous demo

* docker-compose is changed with more attributes
* New Attribues are:
  * build
  * networks
  * volumes

## How to run demo3?

```sh
$ cd demo3
$ docker-compose up -d
# Now follow the same steps to test the microservices as mentioned in Demo1
# let's get the mount path from the flask_service container
$ docker inspect --format='{{json .Mounts}}' <container_id> | python -m json.tool
# Go to volume path and verify that logs being created
# Once that is done, let's check for two way mounting but login to the container
$ docker exec -it <container_id> /bin/sh
# Above command shall take you inside the container
# Now let's go to mounted path /var/local/
$ cd /var/local/
# now let's try and create some files here
$ touch 1 2 3
# Now let's come out of the container gracefully using below command -
# CTRL+P, CTRL+Q
# Once you are our the container then go to the docker volume mount path again
# /var/lib/docker/volumes
$ ls /var/lib/docker/volumes/demo3_flask_app_volume/_data
# now verify that files we created from inside the container are visible here
```

## Few more reference for Topics covered post Demo 2 & 3

* [Docker Compose Volume Reference](https://docs.docker.com/compose/compose-file/compose-file-v2/#volume-configuration-reference)
* [Docker Compose networking](https://docs.docker.com/compose/networking/)
