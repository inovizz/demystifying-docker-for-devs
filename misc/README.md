# Defining a non-root user in Docker file

This demo contains a very basic Dockerfile which defines user.

## Steps to run this Demo and Verify the non-root user

```sh
$ cd misc
$ docker build -t user_demo .
$ docker run -d user_demo
# This would give you a shell, then type following command to verify the user
$ whoami
# Output shall be worker
```
