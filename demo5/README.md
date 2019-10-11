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
Okay, so data is still there. what if we remove container ? lets do that as well. 

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
Oops, data is gone. Now way, i can't afford to lose my data at any cost. 

