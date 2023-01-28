FROM python:3.11.1-slim-buster as build
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    TZ=Europe/Paris \
    POETRY_HOME=/opt/poetry \
    VENV_PATH=/opt/venv \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip && \
    python -m venv $VENV_PATH && \
    $VENV_PATH/bin/pip install poetry && \
    $VENV_PATH/bin/poetry install --no-interaction --no-cache --no-root --without dev -vvv


# FROM python:3.11.1-slim-buster as runtime
# ENV VENV_PATH=/opt/venv \
#     PATH="/opt/venv/bin:$PATH" \
#     PYTHONPATH="/app:$PYHTONPATH"

# WORKDIR /app

# COPY --from=build /app/.venv $VENV_PATH
COPY ./src/aristaeus ./aristaeus
COPY config.toml .

ENV PATH="$VENV_PATH/bin:$PATH" \
    PYTHONPATH="/app:$PYHTONPATH"

EXPOSE 80

# CMD ["tail", "-f", "/dev/null"]
CMD ["uvicorn", "aristaeus.controllers.api.app:create_app", "--host", "0.0.0.0", "--port", "80"]
