FROM python:3.10-slim-bullseye

# sets working directory
WORKDIR /app

#install dependencies
RUN apt-get update && apt-get install -y \
    net-tools \
    curl
    
# copy vertex_app files to container
COPY . /app

# gcloud auth
COPY ultra-function-439306-r4-e46354e08ceb.json /app/ultra-function-439306-r4-e46354e08ceb.json

#certs and key
COPY ssl/certs.pem /etc/ssl/certs/certs.pem
COPY ssl/private.key /etc/ssl/private/private.key

# install modules
RUN pip install --no-cache-dir -r requirements.txt

# ensure cert and key access
RUN chmod 600 /etc/ssl/certs/certs.pem /etc/ssl/private/private.key

# expose port
EXPOSE 8080

# set gcloud app credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="ultra-function-439306-r4-e46354e08ceb.json"

ENV FLASK_APP=app.py

#run command
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app", "--certfile", "/etc/ssl/certs/certs.pem", "--keyfile", "/etc/ssl/private/private.key"]
