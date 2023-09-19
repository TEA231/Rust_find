FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

WORKDIR /usr/src/pars

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/pars/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/pars/
