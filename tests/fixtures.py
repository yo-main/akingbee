import os
import tempfile
from functools import wraps

import pytest
from mock import Mock
from playhouse.sqlite_ext import SqliteExtDatabase

from app import app
from src.data_access.pw_objects import MODELS
from src.data_access.connectors import DB
from src.helpers.helpers import create_new_user


@pytest.fixture(scope="module", autouse=True)
def fake_database():
    DB.drop_tables(MODELS)
    DB.create_tables(MODELS)
    DB.bind(MODELS)
    create_new_user(
        {
            "username": "test",
            "pwd": "123azeAZE",
            "email": "aze@gmail.com"
        }
    )
    return DB


@pytest.fixture(scope="function")
def client():
    app.config["testing"] = True
    with app.test_request_context():
        with app.app_context():
            with app.test_client() as client:
                return client