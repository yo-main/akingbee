import pytest

from fastapi.testclient import TestClient
from gaea.database import db
from gaea.database.utils.test import get_temporary_database
from gaea.models.base import Base
from gaea.webapp import MiddleWare

from cerbes.app import AppClient
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
    client = AppClient(router=router, middleware=middleware)
    yield TestClient(client.get_app())
