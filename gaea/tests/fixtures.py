import pytest
from mock import Mock

from gaea.database import db
from gaea.database.utils.test import get_temporary_database


@pytest.fixture(scope="module")
def test_db():
    with get_temporary_database() as db_url:
        db_client = db(url=db_url)
        yield db_client
        db_client.clear()


class MockRBMQConnectionManager:
    def __init__(self, mocked_channel):
        self.mocked_channel = mocked_channel

    def get_channel(self):
        return self.mocked_channel

    def close(self):
        pass

    def __enter__(self):
        return self.mocked_channel

    def __exit__(self, tp, vl, tb):
        self.mocked_channel.close()
