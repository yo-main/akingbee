import pytest

from src.helpers.users import create_new_user
from src.models.users import User
from src.helpers.tools import _get_trads

from tests.fixtures import client, fake_database, logged_in


@pytest.fixture(scope="module", autouse=True)
def create_a_user(fake_database):
    user = User(username="Bob", pwd="***", email="bob@bobby.bob")
    user.save()


def test_get_setup_page_fail(client):
    answer = client.get("/setup", follow_redirects=True)
    assert answer.status_code == 200
    assert b"<title>aKingBee - \n    Login\n</title>" in answer.data


def test_get_setup_page_success(client):
    logged_in(client)
    answer = client.get("/setup", follow_redirects=True)
    assert answer.status_code == 200
    assert "<title>aKingBee - \n    Paramètre\n</title>".encode() in answer.data


@pytest.mark.parametrize("entity,data_name", [
    ("hive", "owner"),
    ("swarm", "health"),
    ("hive", "conditions"),
    ("hive", "events"),
    ("hive", "honey")
])
def test_create_elements_fail(entity, data_name, client):
    logged_in(client)
    answer = client.post(f"/setup/{entity}/{data_name}", data={"data": ""})
    assert answer.status_code == 500


@pytest.mark.parametrize("entity,data_name", [
    ("hive", "owner"),
    ("swarm", "health"),
    ("hive", "conditions"),
    ("hive", "events"),
    ("hive", "honey")
])
def test_create_elements_success(entity, data_name, client):
    logged_in(client)
    answer = client.post(f"/setup/{entity}/{data_name}", data={"data": "random"})
    assert answer.status_code == 200

    answer = client.get(f"/setup/{entity}/{data_name}", follow_redirects=True)
    assert answer.status_code == 200
    assert b"random" in answer.data


@pytest.mark.parametrize("entity,data_name", [
    ("hive", "owner"),
    ("swarm", "health"),
    ("hive", "conditions"),
    ("hive", "events"),
    ("hive", "honey")
])
def test_modify_elements_success(entity, data_name, client):
    logged_in(client)
    answer = client.put(f"/setup/{entity}/{data_name}", data={"data": "kaboom", "id": 1})
    assert answer.status_code == 200

    answer = client.get(f"/setup/{entity}/{data_name}", follow_redirects=True)
    assert answer.status_code == 200
    assert b"random" not in answer.data
    assert b"kaboom" in answer.data





