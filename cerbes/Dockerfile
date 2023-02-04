FROM python:3.9.1-slim-buster as build
ENV PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    TZ=Europe/Paris \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/opt/venv

ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip && \
    python -m venv $VENV_PATH && \
    $VENV_PATH/bin/pip install poetry && \
    $VENV_PATH/bin/poetry config virtualenvs.create false && \
    $VENV_PATH/bin/poetry install --no-interaction --no-ansi --no-dev -vvv


FROM python:3.9.1-slim-buster as runtime
ENV PYTHONPATH=/app \
    VENV_PATH=/opt/venv
ENV PATH="$VENV_PATH/bin:$PATH"

WORKDIR /app

COPY --from=build $VENV_PATH $VENV_PATH
COPY ./cerbes ./cerbes
COPY config.yaml ./

EXPOSE 9001

CMD ["uvicorn", "cerbes.app:app", "--host", "0.0.0.0", "--port", "9001", "--access-log", "--log-level", "debug"]
