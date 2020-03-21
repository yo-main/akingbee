import pytest
from mock import Mock

from common.redis_client.client import redis


@pytest.fixture()
def mocked_redis_client(monkeypatch):
    mocked = Mock()
    monkeypatch.setattr(redis, "Redis", mocked)
    return mocked
