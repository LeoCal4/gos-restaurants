#
# Docker file for GoOutSafe S4 v1.0
#
FROM python:3.8
LABEL maintainer="GoOutSafe Squad 4 API Gateway"
LABEL version="1.0"
LABEL description="Go Out Safe Application Squad 4"

# creating the environment
COPY . /app
# setting the workdir
WORKDIR /app

# installing all requirements
RUN ["pip", "install", "-r", "requirements.prod.txt"]

# exposing the port
EXPOSE 5000/tcp

# Main command
CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]
