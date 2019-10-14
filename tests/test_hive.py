import datetime

import pytest

from tests.fixtures import client, fake_database, logged_in

from src.constants import alert_codes as alerts
from src.helpers.users import create_new_user
from src.models import Apiary


@pytest.fixture(scope="module", autouse=True)
def setup_database(fake_database):
    create_new_user(
        {
            "username": "test",
            "pwd": "123azeAZE",
            "email": "aze@gmail.com"
        }
    )
    Apiary(
        user_id=1,
        name="tets_apiary",
        status=1,
        birthday=datetime.date.today(),
        location="test_location",
        honey_type=1
    ).save()



def test_get_hive_fail(client):
    answer = client.get("/hive", follow_redirects=True)
    assert answer.status_code == 200
    assert b"<title>aKingBee - \n    Login\n</title>" in answer.data


def test_get_hive_success(client):
    logged_in(client)
    answer = client.get("/hive")
    assert answer.status_code == 200


def test_get_create_hive_page(client):
    logged_in(client)

    answer = client.get("/hive/create")
    assert answer.status_code == 200


@pytest.mark.parametrize("name,birthday,apiary,owner,condition", [
    ("", "19/12/2019", 1, 1, 1),
    ("name", "12/19/2019", 1, 1, 1),
    ("name", "19/12/2019", 9, 1, 1),
    ("name", "19/12/2019", 1, 9, 1),
    ("name", "19/12/2019", 1, 1, 9),
])
def test_create_new_hive_fail(name, birthday, apiary, owner, condition, client):
    logged_in(client)

    data = {
        "name": name,
        "date": birthday,
        "apiary": apiary,
        "owner": owner,
        "hive_condition": condition
    }
    answer = client.post("/hive/create", data=data)
    assert answer.status_code == 500


def test_create_new_hive_success(client):
    logged_in(client)

    data = {
        "name": "test_hive",
        "date": "19/12/2019",
        "apiary": 1,
        "owner": 1,
        "hive_condition": 1
    }
    answer = client.post("/hive/create", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alerts.NEW_HIVE_SUCCESS


def test_create_new_owner_fail(client):
    logged_in(client)
    answer = client.post("/hive/create/new_owner", data={"owner": ""})
    assert answer.status_code == 500


def test_create_new_owner_success(client):
    logged_in(client)
    answer = client.post("/hive/create/new_owner", data={"owner": "Bob"})
    assert answer.status_code == 200
    assert answer.json["code"] == alerts.NEW_BEEKEEPER_SUCCESS


def test_create_new_condition_fail(client):
    logged_in(client)
    data = {"name_fr": "Co", "name_en": ""}
    answer = client.post("/hive/create/new_condition", data=data)
    assert answer.status_code == 500


def test_create_new_condition_success(client):
    logged_in(client)
    data = {"name_fr": "Co", "name_en": "Co"}
    answer = client.post("/hive/create/new_condition", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alerts.NEW_PARAMETER_SUCCESS


def test_get_hive_info_fail(client):
    logged_in(client)
    data = {"bh_id": 10}
    answer = client.post("/hive/get_hive_info", data=data)
    assert answer.status_code == 500


def test_get_hive_info_success(client):
    logged_in(client)
    data = {"bh_id": 1}
    answer = client.post("/hive/get_hive_info", data=data)
    assert answer.status_code == 200
    assert answer.json["id"] == 1


@pytest.mark.parametrize("bh_id,apiary,name,owner", [
    (1, "", 1, 1),
    (1, "apiary", 10, 1),
    (1, "apiary", 1, 10),
    (10, "apiary", 1, 1),
])
def test_modify_hive_fail(bh_id, apiary, name, owner, client):
    logged_in(client)

    data = {
        "bh_id": bh_id,
        "hive": name,
        "apiary": apiary,
        "owner": owner,
    }
    answer = client.post("/hive/submit_hive_info", data=data)
    assert answer.status_code == 500


def test_modify_hive_success(client):
    logged_in(client)

    data = {
        "bh_id": 1,
        "hive": "test_hive_modification",
        "apiary": 1,
        "owner": 1,
    }
    answer = client.post("/hive/submit_hive_info", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alerts.MODIFICATION_SUCCESS

















