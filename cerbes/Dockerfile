FROM python:3.7.7-slim-buster as build
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    TZ=Europe/Paris \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/opt/venv

ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"

COPY poetry.lock pyproject.toml ./

RUN apt-get update && \
    apt-get install -y gcc curl && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    mv /root/.poetry $POETRY_PATH && \
    python -m venv $VENV_PATH && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-dev -vvv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

FROM python:3.7.7-slim-buster as runtime
ENV PYTHONPATH=/app \
    VENV_PATH=/opt/venv
ENV PATH="$VENV_PATH/bin:$PATH"

WORKDIR /app

COPY --from=build $VENV_PATH $VENV_PATH
COPY ./cerbes ./

EXPOSE 9001
