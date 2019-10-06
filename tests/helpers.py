import os
import tempfile
from functools import wraps

import pytest
from mock import Mock
from playhouse.sqlite_ext import SqliteExtDatabase

from app import app
from src.data_access.pw_objects import MODELS
from src.data_access.connectors import DB

@pytest.fixture(scope="session", autouse=True)
def fake_database():
    DB.bind(MODELS)
    DB.create_tables(MODELS)
    return DB


@pytest.fixture
def client():
    app.config["testing"] = True
    with app.test_request_context():
        with app.app_context():
            with app.test_client() as client:
                yield client
