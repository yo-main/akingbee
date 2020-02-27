FROM python:3.7.4-slim-buster

ENV TZ=Europe/Paris
ENV PYTHONPATH /app/src

RUN apt update && apt-get install -y gcc curl
EXPOSE 8080

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN ~/.poetry/bin/poetry config virtualenvs.create false
