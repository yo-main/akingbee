import pytest
from fastapi.testclient import TestClient

from akb.config import settings
from akb.controllers.api.bee.app import create_app

settings.setenv("test")


@pytest.fixture(scope="session")
def app():
    client = TestClient(app=create_app())
    yield client
