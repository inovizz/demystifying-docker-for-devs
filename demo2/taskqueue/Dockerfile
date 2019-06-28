FROM python:3.6-alpine

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true
# define file path for images
ENV FILE_PATH /var/local/

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /queue
WORKDIR /queue


ENTRYPOINT celery -A tasks worker --loglevel=DEBUG