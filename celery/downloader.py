from celery import Celery
import urllib.request
import os

# Where the downloaded files will be stored
BASEDIR="."

# Create the app and set the broker location (RabbitMQ)
app = Celery('downloaderApp',
             backend='redis://redis:6379/0',
             broker='redis://redis:6379/0')

@app.task
def download(url, filename):
    """
    Download a page and save it to the BASEDIR directory
      url: the url to download
      filename: the filename used to save the url in BASEDIR
    """
    response = urllib.request.urlopen(url)
    data = response.read()
    with open(BASEDIR+"/"+filename,'wb') as file:
        file.write(data)
    file.close()

@app.task
def list():
    """ Return an array of all downloaded files """
    return os.listdir(BASEDIR)
