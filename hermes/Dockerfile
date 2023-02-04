FROM python:3.9.15-slim-buster as build
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    TZ=Europe/Paris \
    POETRY_HOME=/opt/poetry \
    VENV_PATH=/opt/venv \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    apt update && apt install -y curl gcc libffi-dev libssl-dev && \
    curl --proto '=https' --tlsv1.3 https://sh.rustup.rs -sSf | bash -s -- -y && \
    pip install cryptography && pip install poetry && \
    poetry export --only=main > requirements.txt

RUN python -m venv $VENV_PATH && \
    $VENV_PATH/bin/pip install -r requirements.txt
# RUN $VENV_PATH/bin/poetry install --no-interaction --no-cache --no-root --without dev -vvv


# FROM python:3.11.1-slim-buster as runtime
# ENV VENV_PATH=/opt/venv \
#     PATH="/opt/venv/bin:$PATH" \
#     PYTHONPATH="/app:$PYHTONPATH"

# WORKDIR /app

# COPY --from=build /app/.venv $VENV_PATH
COPY ./src/hermes ./hermes
COPY config.yaml .

ENV PATH="$VENV_PATH/bin:$PATH" \
    PYTHONPATH="/app:$PYHTONPATH"

EXPOSE 80

# CMD ["tail", "-f", "/dev/null"]
CMD ["python", "hermes/consumer.py"]
