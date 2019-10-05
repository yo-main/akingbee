FROM python:3.7.4-slim-buster

ENV TZ=Europe/Paris
ENV PYTHONPATH /app/akingbee/src

RUN apt update && apt-get install -y gcc
EXPOSE 8080

COPY ./Pipfile* /app/akingbee/
WORKDIR /app/akingbee

RUN pip install pipenv
RUN pipenv install --system