import pytest

from app import create_app
from src.models import MODELS
from src.database import DB, init


@pytest.fixture
def client():
    app = create_app()
    app.config["testing"] = True
    with app.test_client() as client:
        return client


@pytest.fixture(scope="module", autouse=True)
def fake_database():
    init()
    DB.bind(MODELS)
    DB.create_tables(MODELS)
    yield DB
    DB.drop_tables(MODELS)


def logged_in(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["language"] = "fr"
