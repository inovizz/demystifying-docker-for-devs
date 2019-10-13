# Demo5

## Manage data in container

  * Volume
  * Bind Mounts
  * tmpfs
  
## How to run demo5?

**Step 1**: Create a Basic Container 
```sh
arunc@arun:~$ docker container run -it --name mortal busybox sh
Unable to find image 'busybox:latest' locally
latest: Pulling from library/busybox
7c9d20b9b6cd: Pull complete 
Digest: sha256:fe301db49df08c384001ed752dff6d52b4305a73a7f608f21528048e8a08b51e
Status: Downloaded newer image for busybox:latest
/ # 
```

**Step 2**: Create some file and append something into it.
```sh
/ # touch someinfo.txt
/ # echo "This might be some useful information." >> someinfo.txt 
/ # cat someinfo.txt 
This might be some useful information.
```

**Step 3**: let's see where it is getting stored (Anyways it would be somewhere on the host itself). Therefore, it's time to inspect and i love doing that :) 
```sh
arunc@arun:~$ docker inspect --format='{{json .GraphDriver}}' 35a93cb4bfab
{
  "Data": {
    "LowerDir": "/var/lib/docker/overlay2/8bc94f4c70a6099cb8b3ea798c934ccbaa5a1570dcecab31f917288366319f7b-init/diff:/var/lib/docker/overlay2/138eef034e690e4ab930d4d028ce96379372a68c44d37474a41bd765c936e3fb/diff",
    "MergedDir": "/var/lib/docker/overlay2/8bc94f4c70a6099cb8b3ea798c934ccbaa5a1570dcecab31f917288366319f7b/merged",
    "UpperDir": "/var/lib/docker/overlay2/8bc94f4c70a6099cb8b3ea798c934ccbaa5a1570dcecab31f917288366319f7b/diff",
    "WorkDir": "/var/lib/docker/overlay2/8bc94f4c70a6099cb8b3ea798c934ccbaa5a1570dcecab31f917288366319f7b/work"
  },
  "Name": "overlay2"
}
```

**Step 4**: Watch out for `UpperDir`  
```sh
root@arun:~# hostname
arun.net <-- I am in the host now. Not in the container. 

root@arun:~# ls -al /var/lib/docker/overlay2/8bc94f4c70a6099cb8b3ea798c934ccbaa5a1570dcecab31f917288366319f7b/diff
total 16
drwxr-xr-x 3 root root 4096 Oct 11 08:06 .
drwx------ 5 root root 4096 Oct 11 08:02 ..
drwx------ 2 root root 4096 Oct 11 08:06 root
-rw-r--r-- 1 root root   39 Oct 11 08:06 someinfo.txt

root@arun:~# cat /var/lib/docker/overlay2/8bc94f4c70a6099cb8b3ea798c934ccbaa5a1570dcecab31f917288366319f7b/diff/someinfo.txt 
This might be some useful information.
```

So we got it and this is where the container's data is getting stored. 

Alright, It's time to do some experiments:

**Step 5**: Stop the container and see if data persist.
```sh
arunc@arun:~$ docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
35a93cb4bfab        busybox             "sh"                36 minutes ago      Up 36 minutes                           mortal

arunc@arun:~$ docker container stop 35a93cb4bfab
35a93cb4bfab

root@arun:~# cat /var/lib/docker/overlay2/8bc94f4c70a6099cb8b3ea798c934ccbaa5a1570dcecab31f917288366319f7b/diff/someinfo.txt 
This might be some useful information.
```
Okay, so data is still there. what if we remove container? lets do that as well. 

**Step 6**: Remove Container
```sh
arunc@arun:~$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                       PORTS               NAMES
35a93cb4bfab        busybox             "sh"                39 minutes ago      Exited (137) 2 minutes ago                       mortal

arunc@arun:~$ docker container rm 35a93cb4bfab
35a93cb4bfab
```

Step 7: Is my data there?
```sh
root@arun:~# cat /var/lib/docker/overlay2/8bc94f4c70a6099cb8b3ea798c934ccbaa5a1570dcecab31f917288366319f7b/diff/someinfo.txt 
cat: /var/lib/docker/overlay2/8bc94f4c70a6099cb8b3ea798c934ccbaa5a1570dcecab31f917288366319f7b/diff/someinfo.txt: No such file or directory
```
Oops, data is gone. No way, i can't afford to lose my data at any cost. 


### Volume is the saviour.

Alright, it sounds interesting but how to use that?

`--v` or `--volume`  flag can be leveraged to use volume.  we also have got `--mount` flag as well. lets discuss it later on.

**Step 1**:  Create a basic container with a volume attached to it at some specific location inside a container. For eg: `/var/www/logs`.
```sh
arunc@arun:~$ docker container run -itd --name sweet_container -v /var/www/logs busybox sh
e3a3bcc3817e2a34f7a7daad0e7c761138da003937b2231d847791f92a921b79
```

**Step 2**:  Find out where exactly is the volume. Time to inspect again. 
```sh
arunc@arun:~$ docker inspect --format='{{json .Mounts}}' e3a3bcc3817e
{
  "Type": "volume",
  "Name": "37a2c4c8f33ad23eb6273d14ecad5bf8f8d257c897cae019573df9fc2b5613df",
  "Source": "/var/lib/docker/volumes/37a2c4c8f33ad23eb6273d14ecad5bf8f8d257c897cae019573df9fc2b5613df/_data",
  "Destination": "/var/www/logs",
  "Driver": "local",
  "Mode": "",
  "RW": true,
  "Propagation": ""
}
```
Alright, we've got the source and destination. let's do some experiments. 

**Step 3**: Create some file and append something into it.  
```sh
arunc@arun:~$ docker container ls 
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
e3a3bcc3817e        busybox             "sh"                9 minutes ago       Up 9 minutes                            sweet_container

arunc@arun:~$ docker attach e3a3bcc3817e
/ # cd /var/www/logs/
/var/www/logs # touch a.txt
/var/www/logs # echo "Some useful information" >> a.txt 
/var/www/logs # cat a.txt 
Some useful information
```

**Step 4**: Validate the above information at the source and try creating some file from host as well and see if it appears inside container.
```sh
root@arun# hostname
arun.net  <=== Note: I am in host now, not in container. 

root@arun:~# cd /var/lib/docker/volumes/37a2c4c8f33ad23eb6273d14ecad5bf8f8d257c897cae019573df9fc2b5613df/_data

root@arun:/var/lib/docker/volumes/37a2c4c8f33ad23eb6273d14ecad5bf8f8d257c897cae019573df9fc2b5613df/_data# ls -al
total 12
drwxr-xr-x 2 root root 4096 Oct 11 09:16 .
drwxr-xr-x 3 root root 4096 Oct 11 09:06 ..
-rw-r--r-- 1 root root   24 Oct 11 09:16 a.txt

root@arun:/var/lib/docker/volumes/37a2c4c8f33ad23eb6273d14ecad5bf8f8d257c897cae019573df9fc2b5613df/_data# cat a.txt 
Some useful information

root@arun:/var/lib/docker/volumes/37a2c4c8f33ad23eb6273d14ecad5bf8f8d257c897cae019573df9fc2b5613df/_data# touch b.txt

root@arun:/var/lib/docker/volumes/37a2c4c8f33ad23eb6273d14ecad5bf8f8d257c897cae019573df9fc2b5613df/_data# echo "Some more information" >> b.txt

root@arun:/var/lib/docker/volumes/37a2c4c8f33ad23eb6273d14ecad5bf8f8d257c897cae019573df9fc2b5613df/_data# cat b.txt 
Some more information
```
**Step 5**: Login to the container and see if `b.txt` is there.
```sh
arunc@arun:~$ docker container ls 
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
e3a3bcc3817e        busybox             "sh"                17 minutes ago      Up 17 minutes                           sweet_container

arunc@arun:~$ docker attach e3a3bcc3817e

/var/www/logs # ls -al
total 16
drwxr-xr-x    2 root     root          4096 Oct 11 03:48 .
drwxr-xr-x    1 root     root          4096 Oct 11 03:36 ..
-rw-r--r--    1 root     root            24 Oct 11 03:46 a.txt
-rw-r--r--    1 root     root            22 Oct 11 03:48 b.txt

/var/www/logs # cat b.txt 
Some more information
``` 
So with this, it is clear that data can be written at `Source` and `Destination` as well. Although, it is not recommended to mangle directly with the `source` as it is something which managed via docker. 

Take a look at the `Step 2` above and notice the name. Don't you think it's not that easy to remember that hash as the name? what if, we could give some fancy name to the volume? Is that possible? 

The short answer is Yes, it's quite possible. Let's see how:

### Create and Manage Volumes 

**Step 1**: Create a volume
```sh
arunc@arun:~$ docker volume create my-volume
my-volume
```

**Step 2**: List volumes
```sh
arunc@arun:~$ docker volume ls
DRIVER              VOLUME NAME
local               37a2c4c8f33ad23eb6273d14ecad5bf8f8d257c897cae019573df9fc2b5613df
local               my-volume
```

**Step 3**: Inspect a volume
```sh
arunc@arun:~$ docker volume inspect my-volume
[
    {
        "CreatedAt": "2019-10-11T09:54:15+05:30",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/my-volume/_data",
        "Name": "my-volume",
        "Options": {},
        "Scope": "local"
    }
]
```

**Step 4**: Start a container with a volume
```sh
arunc@arun:~$ docker container run -itd --name sweet_container -v my-volume:/var/www/logs busybox sh
9b66dabe77b95afba17c1886f39722fb0e4fd662a9daca8178cc772c4d6d7051

arunc@arun:~$ docker container ls 
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
9b66dabe77b9        busybox             "sh"                11 seconds ago      Up 9 seconds                            sweet_container

arunc@arun:~$ docker inspect --format='{{json .Mounts}}' 9b66dabe77b9
{
  "Type": "volume",
  "Name": "my-volume",
  "Source": "/var/lib/docker/volumes/my-volume/_data",
  "Destination": "/var/www/logs",
  "Driver": "local",
  "Mode": "z",
  "RW": true,
  "Propagation": ""
}
```

**Step 5**: Lets play data data 
```sh
arunc@arun:~$ docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
9b66dabe77b9        busybox             "sh"                3 minutes ago       Up 3 minutes                            sweet_container

arunc@arun:~$ docker attach 9b66dabe77b9

/ # cd /var/www/logs/

/var/www/logs # touch a.log

/var/www/logs # date >> a.log

/var/www/logs # cat a.log 
Fri Oct 11 04:34:08 UTC 2019
```

**Step 6**: Stop and Remove container 
```sh
arunc@arun:~$ docker container stop 9b66dabe77b9
9b66dabe77b9

arunc@arun:~$ docker container rm 9b66dabe77b9
9b66dabe77b9

arunc@arun:~$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

arunc@arun:~$ 
```

**Step 7**: Did i just lose my data along with the container? Lets see:
```sh
root@arun:/var/lib/docker/volumes/my-volume/_data# pwd; ls -al
--- /var/lib/docker/volumes/my-volume/_data
total 12
drwxr-xr-x 2 root root 4096 Oct 11 10:04 .
drwxr-xr-x 3 root root 4096 Oct 11 09:54 ..
-rw-r--r-- 1 root root   29 Oct 11 10:04 a.log

root@arun:/var/lib/docker/volumes/my-volume/_data# cat a.log 
Fri Oct 11 04:34:08 UTC 2019
```
Oh yes, my data is intact.Thus, Volumes exists independently of containers.  
