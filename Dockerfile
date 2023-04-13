FROM python:3.10.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /tsp-api

WORKDIR /tsp-api

ADD . /tsp-api

RUN pip install -r requirements.txt