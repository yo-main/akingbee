import pytest
from mock import Mock, MagicMock, AsyncMock

from fastapi.testclient import TestClient
from gaea.database import db
from gaea.database.utils.test import get_temporary_database
from gaea.rbmq.base import RBMQConnectionManager
from gaea.models.base import Base
from gaea.models.utils.test import DATASETS, IDS
from gaea.webapp import MiddleWare, AppClient

from aristaeus.api.v1 import ROUTERS
from aristaeus.helpers import authentication


@pytest.fixture(scope="module")
def test_db():
    with get_temporary_database() as url:
        db_client = db(url=url)
        Base.metadata.create_all(bind=db_client.engine)

        with db_client as session:
            for dataset in DATASETS:
                session.bulk_save_objects(dataset)
                session.commit()

        yield db_client
        db_client.clear()


@pytest.fixture(scope="module")
def test_app(test_db):  # pylint: disable=redefined-outer-name
    routers = ROUTERS
    middleware = MiddleWare(db_client=test_db)
    client = AppClient(routers=routers, middleware=middleware)
    yield TestClient(client.get_app())

@pytest.fixture
def auth_token(monkeypatch):
    mocked_results = {"user_id": str(IDS["Users"][0])}
    monkeypatch.setattr(authentication, "validate_access_token", AsyncMock(return_value=mocked_results))
    return "token"

@pytest.fixture()
def mock_rbmq_channel(monkeypatch):
    mocked_channel = Mock()
    mocked_conn = Mock()
    monkeypatch.setattr(mocked_conn, "channel", MagicMock(return_value=mocked_channel))
    monkeypatch.setattr(RBMQConnectionManager, "_get_connection", MagicMock(return_value=mocked_conn))
    return mocked_channel
