FROM yomain/akingbee:engine

ENV PYTHONPATH /app/src

WORKDIR /app
COPY . /app

RUN poetry install --no-dev
