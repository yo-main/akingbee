import pytest

from app import app
from src.models import MODELS
from src.database import DB


@pytest.fixture(scope="module", autouse=True)
def fake_database():
    DB.bind(MODELS)
    DB.create_tables(MODELS)
    yield DB
    DB.drop_tables(MODELS)


@pytest.fixture
def client():
    app.config["testing"] = True
    with app.test_client() as client:
        return client


def logged_in(client):
    with client.session_transaction() as session:
        session["user_id"] = 1

