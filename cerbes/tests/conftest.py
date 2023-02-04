import pytest
from gaea.config import CONFIG
from mock import MagicMock, Mock

CONFIG.setenv("test")

from fastapi.testclient import TestClient
from gaea.database import db
from gaea.database.utils.test import get_temporary_database
from gaea.models.base import Base
from gaea.rbmq.base import RBMQConnectionManager
from gaea.webapp import AppClient, MiddleWare

from cerbes.views import router


@pytest.fixture(scope="module")
def test_db():
    with get_temporary_database() as url:
        db_client = db(url=url)
        Base.metadata.create_all(bind=db_client.engine)
        yield db_client
        db_client.clear()


@pytest.fixture(scope="module")
def test_app(test_db):  # pylint: disable=redefined-outer-name
    middleware = MiddleWare(db_client=test_db)
    client = AppClient(routers=router, middleware=middleware)
    yield TestClient(client.get_app())


@pytest.fixture()
def mock_rbmq_channel(monkeypatch):
    mocked_channel = Mock()
    mocked_conn = Mock()
    monkeypatch.setattr(mocked_conn, "channel", MagicMock(return_value=mocked_channel))
    monkeypatch.setattr(
        RBMQConnectionManager, "_get_connection", MagicMock(return_value=mocked_conn)
    )
    return mocked_channel
