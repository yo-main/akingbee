FROM python:3.9.15-buster as build
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    TZ=Europe/Paris \
    VENV_PATH=/opt/venv

WORKDIR /app

COPY requirements.txt .

RUN python -m venv $VENV_PATH && $VENV_PATH/bin/pip install wheel && \
    $VENV_PATH/bin/pip install -r requirements.txt


FROM python:3.9.15-slim-buster as runtime

ENV VENV_PATH=/opt/venv \
    TZ=Europe/Paris \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app:$PYHTONPATH"

WORKDIR /app

COPY --from=build $VENV_PATH $VENV_PATH
COPY ./src/hermes ./hermes
COPY config.yaml .

EXPOSE 80

CMD ["python", "hermes/consumer.py"]
