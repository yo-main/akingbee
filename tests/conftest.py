import pytest
from mock import Mock, MagicMock, patch
from peewee import SqliteDatabase

from common.redis_client.client import redis
from common.models import MODELS, User
from common.database.connectors import DB

database = SqliteDatabase(":memory:", pragmas=(("foreign_keys", 1),))
DB.initialize(database)
DB.bind(MODELS)
DB.create_tables(MODELS)

@pytest.fixture()
def mocked_redis_client(monkeypatch):
    mocked = Mock()
    monkeypatch.setattr(redis, "Redis", mocked)
    return mocked

