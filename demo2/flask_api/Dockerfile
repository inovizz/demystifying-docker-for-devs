FROM python:3.6-alpine

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

ENV HOST 0.0.0.0
ENV PORT 5001
ENV DEBUG true

COPY requirements.txt requirements.txt

# expose the app port
EXPOSE 5001

# install requirements
RUN pip install -r requirements.txt

WORKDIR /api
COPY . /api

#  DEFINED LOG BASE PATH
ENV LOG_BASE_PATH /var/local/

# run the app server
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "3", "app:app"]

# Docker file reference documentation - https://docs.docker.com/engine/reference/builder/