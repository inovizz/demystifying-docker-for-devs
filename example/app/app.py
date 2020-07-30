
from flask import Flask
from flask import render_template
from flask import request, url_for

from redis import StrictRedis
from datetime import datetime
from worker import task_queue

import logging
import os
from logging.handlers import RotatingFileHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(os.path.join(os.environ.get(
    'LOG_BASE_PATH'), 'flask_app.log'), maxBytes=10000)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
redis = StrictRedis(host='backend', port=6379)


@app.route('/')
def home():
    redis.lpush('times', datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'))
    return render_template('index.html', title='Home',
                           times=redis.lrange('times', 0, -1))

@app.route('/download', methods=['POST'])
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
        logger.info("Current status of task id {} is {}".format(
            task_id, res.state))
        return res.state

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
