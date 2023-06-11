FROM python:3.11-buster as build
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    TZ=Europe/Paris \
    POETRY_HOME=/opt/poetry \
    VENV_PATH=/opt/venv \
    POETRY_VIRTUALENVS_CREATE=false

COPY requirements.txt .

RUN python -m venv $VENV_PATH && $VENV_PATH/bin/pip install wheel && \
    $VENV_PATH/bin/pip install -r requirements.txt



FROM python:3.11-slim-buster as runtime
ENV VENV_PATH=/opt/venv \
    TZ=Europe/Paris \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app:$PYHTONPATH"

RUN apt update && apt install -y libpq-dev

WORKDIR /app

COPY --from=build $VENV_PATH $VENV_PATH
COPY src/aristaeus aristaeus
COPY config.toml config.toml
COPY alembic.ini alembic.ini
COPY migrations migrations
COPY scripts/entrypoint.sh /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]

CMD [
    "uvicorn",
    "--host",
    "0.0.0.0",
    "--port",
    "80",
    "--proxy-headers",
    "--workers",
    "4",
    "aristaeus.controllers.api.app:create_app"
]
