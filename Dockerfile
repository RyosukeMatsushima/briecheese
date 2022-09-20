FROM python:3.10

RUN apt-get update && apt-get upgrade -y
RUN pip3 install --upgrade pip setuptools

# DB
RUN apt-get install -y python3-dev default-libmysqlclient-dev
RUN pip3 install mysqlclient

RUN apt-get clean

