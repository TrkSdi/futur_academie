# syntax = docker/dockerfile:experimental

FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt-get install -y libgdal-dev libffi-dev curl

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY /src .env /code/
COPY .env /code/src