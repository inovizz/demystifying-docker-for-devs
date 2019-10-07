# Documentation for Flask API and Celery Microservice

We'll be using two microservices basically in this Workshop all through the four demos. I'll try and explain each of them here so that we don't have to spend too much time understanding the Microservices, or the code at the time of demo.

## Flask_api Microservice

This is a very simple web API written in Flask. if you look at the file "app.py" there are three API endpoints defined and their respective functions are given.

1. <b>/ (root)</b> - The root API basically is un-related from the next two API endpoints. This [example](https://docs.docker.com/get-started/part2/) is taken from docs.docker.com. This function basically tries to increase the value of a key called "counter" in redis DB. If it is not able to connect to redis then it throws an exception.

2. <b>/download/</b> API - This API gets a file_name and an image_url in a POST request and this function send this image download task to celery which adds it into its redis queue, which in return provides the task id.

3. <b>/check/<task_id>/</b> - This API checks for the status of the task by passing the <task_id> in the URL. The function returns the status of the task in response.

## Taskqueue Microservice

This is a supportive microservice to the first one - flask_api and flask_api would call this microservice to spawn celery workers for image download task as defined above. So to understand this one, let's take a look at file called - tasks.py

This majorily has two things -

1. We are defining the celery broker and also the result backend
2. We have also defined a function called "download" which gets called when we hit /download API in flask_api microserice. From a functionality standpoint it receives the image_url to download and then celery worker perform the task and store it a defined directory with the given file name.

In case you are not familiar and may want to read about Celery and Redis, then please refer the offical documentation given below -

- [Celery Docs](https://docs.celeryproject.org/en/latest/)
- [Redis Docs](https://redis.io/documentation)
