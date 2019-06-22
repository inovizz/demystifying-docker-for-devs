from flask import Flask
from flask import url_for
from flask import request
from flask import jsonify
from worker import celery
import celery.states as states
from redis import Redis, RedisError
import os
import redis
import socket
import logging

app = Flask(__name__)

rcon = redis.StrictRedis(host="redis", db=0, decode_responses=True)

@app.route('/download/', methods=['GET', 'POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    task = celery.send_task('tasks.download',
                            args=[url], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response

@app.route('/check/<task_id>')
def check_task(task_id):
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)

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