# syntax = docker/dockerfile:experimental

FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt-get install -y libgdal-dev libffi-dev curl

RUN mkdir /code

WORKDIR /code
COPY ./.env /code/

COPY requirements.txt /code/
# RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN pip install -r requirements.txt
COPY /src /code/
COPY .env /code/
RUN ls -l