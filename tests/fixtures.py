import os
import tempfile
from functools import wraps

import pytest
from mock import Mock, MagicMock
from peewee import SqliteDatabase

from app import app
from src.models import MODELS
from src.database import DB
from src.helpers.users import create_new_user

@pytest.fixture(scope="module", autouse=True)
def fake_database():
    DB.bind(MODELS)
    DB.create_tables(MODELS)
    yield DB
    # DB.drop_tables(MODELS)


@pytest.fixture(scope="function")
def client():
    app.config["testing"] = True
    with app.test_client() as client:
        return client