import logging
import os
import socket

import celery.states as states
import redis
from flask import Flask, jsonify, request, url_for
from redis import Redis, RedisError

from worker import task_queue

app = Flask(__name__)

rcon = redis.StrictRedis(host="redis", db=0, decode_responses=True)

@app.route('/download/', methods=['GET', 'POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    task = task_queue.send_task('tasks.download',
                            args=[url], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response

@app.route('/check/<task_id>')
def check_task(task_id):
    res = task_queue.AsyncResult(task_id)
    if res:
        return res.state

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
