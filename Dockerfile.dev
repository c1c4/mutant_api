FROM python:3.8-slim-buster

WORKDIR /mutant_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /mutant_api/requirements.txt
RUN pip install -r requirements.txt

COPY . /mutant_api
