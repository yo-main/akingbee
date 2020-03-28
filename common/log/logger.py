import os
import time
import json
import uuid
import datetime
import logging
from logging.handlers import RotatingFileHandler

import flask

from common.config import CONFIG


class ContextFilter(logging.Filter):
    def filter(self, record):
        if flask.has_request_context():
            # when logging out, the user_id is already set
            if not hasattr(record, "user_id"):
                record.user_id = flask.session.get("user_id") or "guest"

            record.request_form = {
                key: item
                for key, item in flask.request.form.items()
                if key not in ("password", "pwd")
            }

            record.request_id = uuid.uuid4()
            record.request_path = flask.request.path
            record.request_method = flask.request.method
            record.request_user_agent = flask.request.user_agent
            record.request_ip_address = flask.request.remote_addr
        return True


class CustomLogger(logging.Logger):
    """Custom logger"""

    def debug(self, msg, *args, **kwargs):
        self._log(logging.DEBUG, msg, args, extra=kwargs)

    def info(self, msg, *args, **kwargs):
        self._log(logging.INFO, msg, args, extra=kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log(logging.WARNING, msg, args, extra=kwargs)

    def critical(self, msg, *args, **kwargs):
        self._log(logging.CRITICAL, msg, args, extra=kwargs)

    def error(self, msg, *args, exc_info=None, **kwargs):
        self._log(logging.ERROR, msg, args, exc_info=exc_info, extra=kwargs)

    def exception(self, msg, *args, **kwargs):
        self._log(logging.ERROR, msg, args, exc_info=True, extra=kwargs)


EXCLUDED_FIELDS = (
    "msg",
    "asctime",
    "args",
    "filename",
    "module",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "levelno",
)


class CustomFormatter(logging.Formatter):
    converter = time.gmtime

    def formatTime(self, record, datefmt):
        return datetime.datetime.fromtimestamp(
            record.created, tz=datetime.timezone.utc
        ).isoformat()

    def format(self, record):
        record.message = record.getMessage()
        setattr(record, "@timestamp", self.formatTime(record, self.datefmt))

        log_data = {
            key: item
            for key, item in record.__dict__.items()
            if item is not None and key not in EXCLUDED_FIELDS
        }

        return json.dumps(log_data, default=str)


logger = CustomLogger(os.environ.get("SERVICE_NAME"))
logger.setLevel(logging.DEBUG)


formatter = CustomFormatter(datefmt="%Y-%m-%dT%H:%M:%S")


if CONFIG.ENV != "TEST":
    log_path = os.path.join(CONFIG.PATH_LOGS, CONFIG.LOGS_FILE_NAME)
    file_handler = RotatingFileHandler(log_path, "a", 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(
    logging.Formatter(
        fmt="{asctime} | {levelname:8s} | {message}",
        datefmt="%Y-%m-%dT%H:%M:%S",
        style="{",
    )
)
logger.addHandler(stream_handler)


def init_logging_filter():
    context_filter = ContextFilter()
    logger.addFilter(context_filter)
