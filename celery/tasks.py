from celery import Celery
import urllib.request
import os
import uuid

# Where the downloaded files will be stored
BASEDIR="."

CELERY_BROKER_URL = os.environ.get(
    'CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379')

app = Celery('downloaderApp',
             backend=CELERY_RESULT_BACKEND,
             broker=CELERY_BROKER_URL)

@app.task(name='tasks.download')
def download(url):
    """
    Download a page and save it to the BASEDIR directory
      url: the url to download
    """
    response = urllib.request.urlopen(url)
    data = response.read()
    with open(BASEDIR+"/"+str(uuid.uuid4().hex),'wb') as file:
        file.write(data)
    file.close()

@app.task(name='tasks.download')
def list():
    """ Return an array of all downloaded files """
    return os.listdir(BASEDIR)
