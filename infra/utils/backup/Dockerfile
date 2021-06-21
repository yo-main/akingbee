FROM python:3.9.1-slim-buster as build
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


FROM python:3.9.1-slim-buster as runtime
ENV PYTHONPATH=/app \
    VENV_PATH=/opt/venv
ENV PATH="$VENV_PATH/bin:$PATH"

RUN apt-get update && apt-get -y install lsb-release wget gnupg \
    && echo deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update && apt-get -y install postgresql-client-12

WORKDIR /app

COPY --from=build $VENV_PATH $VENV_PATH
COPY ./backup.py ./backup.py

CMD ["./backup.py"]
