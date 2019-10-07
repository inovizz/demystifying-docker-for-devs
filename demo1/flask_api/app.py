# native imports
import logging
import os
import socket
from logging.handlers import RotatingFileHandler

# third party imports
import celery.states as states
import redis
from flask import Flask, jsonify, request, url_for
from redis import Redis, RedisError

# import celery worker
from worker import task_queue

# initial the flask app
app = Flask(__name__)

# initiate redis connection
rcon = redis.StrictRedis(host="redis", db=0, decode_responses=True)


@app.route("/")
def redis_counter():
    try:
        visits = rcon.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)


@app.route('/download/', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    file_name = data.get('file_name', '')
    task = task_queue.send_task('tasks.download',
                                args=[url, file_name], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response


@app.route('/check/<task_id>')
def check_task(task_id):
    res = task_queue.AsyncResult(task_id)
    if res:
        return res.state


if __name__ == "__main__":
    # Run the app on port 5001
    app.run(host='0.0.0.0', port=5001, debug=True)
