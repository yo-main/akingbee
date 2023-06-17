FROM python:3.11-buster as build
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    TZ=Europe/Paris \
    VENV_PATH=/opt/venv

COPY requirements.txt .

RUN python -m venv $VENV_PATH && $VENV_PATH/bin/pip install wheel && \
    $VENV_PATH/bin/pip install -r requirements.txt


FROM python:3.11-slim-buster as runtime

ENV VENV_PATH=/opt/venv \
    TZ=Europe/Paris \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app:$PYHTONPATH"

WORKDIR /app

COPY --from=build $VENV_PATH $VENV_PATH
COPY ./src/hermes ./hermes
COPY config.yaml .

CMD ["python", "hermes/consumer.py"]
