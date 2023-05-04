FROM python:3.10-slim
ENV PYTHONBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/requirements.txt
COPY . /code/
RUN apt-get update && apt-get -y install python-dev default-mysql-client default-libmysqlclient-dev libssl-dev &&\
    pip install -r requirements.txt
