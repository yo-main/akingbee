import os
import tempfile
from functools import wraps

import pytest
from mock import Mock
from playhouse.sqlite_ext import SqliteExtDatabase

from app import app
from src.data_access.pw_objects import MODELS


DATABASES = {}


def use_database(name="_default"):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            with DATABASES[name].bind_ctx(MODELS):
                DATABASES[name].create_tables(MODELS)
                res = func(*args, **kwargs)
            return res
        return inner
    if name not in DATABASES:
        DATABASES[name] = SqliteExtDatabase(":memory:")
    return wrapper


@pytest.fixture
def client():
    app.config["testing"] = True
    with app.test_request_context():
        with app.app_context():
            with app.test_client() as client:
                yield client
