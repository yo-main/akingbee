FROM yomain/akingbee:engine

COPY . /app
WORKDIR /app

RUN ~/.poetry/bin/poetry install --no-dev
