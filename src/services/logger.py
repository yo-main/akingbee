import os
import logging
from logging.handlers import RotatingFileHandler

import flask

from src.constants import environments


class ContextFilter(logging.Filter):
    def filter(self, record):
        user_id = "guest"
        if flask.request:
            user_id = flask.session.get("user_id") or "guest"
        record.user_id = user_id
        return True


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_format = (
    "{asctime:25} :: {levelname:>5} :: {filename:>15} :: "
    "{funcName:>15} :: {user_id:>4} :: {message}"
)
formatter = logging.Formatter(log_format, style="{")

context_filter = ContextFilter()
logger.addFilter(context_filter)

if environments.PLATFORM_ENVIRONMENT != "TEST":
    log_path = os.path.join(environments.LOG_DIRECTORY, environments.ACTIVITY_LOG)
    file_handler = RotatingFileHandler(log_path, "a", 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
