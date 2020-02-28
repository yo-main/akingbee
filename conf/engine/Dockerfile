FROM python:3.7.4-slim-buster

ENV TZ=Europe/Paris
ENV POETRY_PATH=/opt/poetry
ENV PATH="$POETRY_PATH/bin:$PATH"

RUN apt-get update && apt-get install -y gcc curl
EXPOSE 8080

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    mv /root/.poetry $POETRY_PATH
RUN poetry config virtualenvs.create false
