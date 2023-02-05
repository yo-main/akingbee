FROM python:3.9.15-buster as build
ENV PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    TZ=Europe/Paris \
    VENV_PATH=/opt/venv

COPY requirements.txt .

RUN python -m venv $VENV_PATH && $VENV_PATH/bin/pip install wheel && \
    $VENV_PATH/bin/pip install -r requirements.txt


FROM python:3.9.15-slim-buster as runtime

ENV VENV_PATH=/opt/venv \
    TZ=Europe/Paris \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app:$PYHTONPATH"

RUN apt update && apt install -y libpq-dev

WORKDIR /app

COPY --from=build $VENV_PATH $VENV_PATH
COPY cerbes cerbes
COPY config.yaml config.yaml
COPY alembic.ini alembic.ini
COPY migratons migrations
COPY scripts/entrypoint.sh /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "cerbes.app:app", "--host", "0.0.0.0", "--port", "80", "--access-log", "--log-level", "debug"]
