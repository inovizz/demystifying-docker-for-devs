import os
import time
import urllib.request

from celery import Celery

# Where the downloaded files will be stored
BASEDIR = os.environ.get('FILE_PATH', '.')

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

queue = Celery('downloaderApp', backend=CELERY_RESULT_BACKEND,
               broker=CELERY_BROKER_URL)


@queue.task(name='tasks.download')
def download(url, file_name):
    """
    Download a page and save it to the BASEDIR directory
      url: the url to download
    """
    time.sleep(10)
    current_time = str(time.time())
    response = urllib.request.urlopen(url)
    data = response.read()
    with open(BASEDIR+"/"+file_name+'_'+current_time, 'wb') as file:
        file.write(data)
