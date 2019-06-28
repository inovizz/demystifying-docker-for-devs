import logging
import os
import socket
from logging.handlers import RotatingFileHandler

import celery.states as states
import redis
from flask import Flask, jsonify, request, url_for
from redis import Redis, RedisError

from worker import task_queue

app = Flask(__name__)

############# Added Logging ####################
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(os.path.join(os.environ.get('LOG_BASE_PATH'), 'flask_app.log'), maxBytes=10000)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
################################################

rcon = redis.StrictRedis(host="redis", db=0, decode_responses=True)

@app.route('/download/', methods=['GET', 'POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    file_name = data.get('file_name', '')
    logger.info("Download request received for URL - {}".format(url))
    task = task_queue.send_task('tasks.download',
                                args=[url, file_name], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response

@app.route('/check/<task_id>')
def check_task(task_id):
    res = task_queue.AsyncResult(task_id)
    if res:
        logger.info("Current status of task id {} is {}".format(task_id, res.state))
        return res.state

@app.route("/")
def redis_counter():
    try:
        visits = rcon.incr("counter")
        logger.info("Redis Counter has been increased, the cntr value is {}".format(rcon.get('counter')))
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
