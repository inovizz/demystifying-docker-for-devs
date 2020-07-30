FROM python:3.7-alpine
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
ENV LOG_BASE_PATH /var/local/
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
CMD ["python3", "app.py"]
