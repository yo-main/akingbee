import datetime

import pytest
import flask

import peewee

from tests.fixtures import client, fake_database, logged_in

from src.constants import alert_codes
from src.helpers.users import create_new_user
from src.models import User


@pytest.fixture(scope="module", autouse=True)
def create_a_user():
    create_new_user(
        {
            "username": "test",
            "pwd": "123azeAZE",
            "email": "aze@gmail.com"
        }
    )


@pytest.mark.parametrize("name,location,honey,status,expected", [
    ("", "Location", "1", "1", alert_codes.MISSING_INFORMATION_APIARY),
    ("Name", "", "1", "1", alert_codes.MISSING_INFORMATION_APIARY),
    ("Name", "Location", "", "1", alert_codes.MISSING_INFORMATION_APIARY),
    ("Name", "Location", "1", "", alert_codes.MISSING_INFORMATION_APIARY),
    ("Name", "Location", "9", "1", alert_codes.INCONSISTANT_DATA),
    ("Name", "Location", "1", "5", alert_codes.INCONSISTANT_DATA),
])
def test_create_apiary_fail(name, location, honey, status, expected, client):
    logged_in(client)

    data = {
        "name": name,
        "location": location,
        "honey_type": honey,
        "status": status,
        "birthday": "01/01/2019",
    }
    answer = client.post("/apiary/create", data=data)
    assert answer.status_code == 500
    assert answer.json["code"] == expected


def test_create_apiary_success(client):
    logged_in(client)

    data = {
        "name": "apiary",
        "location": "here",
        "honey_type": "1",
        "status": "1",
        "birthday": "01/01/2019",
    }
    answer = client.post("/apiary/create", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.NEW_APIARY_SUCCESS


def test_create_new_apiary_status_fail(client):
    logged_in(client)

    data = {"name_fr": "test", "name_en": ""}
    answer = client.post("/apiary/create/new_apiary_status", data=data)
    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.INCONSISTANT_DATA


def test_create_new_apiary_status_success(client):
    logged_in(client)

    data = {"name_fr": "test", "name_en": "te"}
    answer = client.post("/apiary/create/new_apiary_status", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.NEW_PARAMETER_SUCCESS


def test_create_new_honey_type_fail(client):
    logged_in(client)

    data = {"name_fr": "test", "name_en": ""}
    answer = client.post("/apiary/create/new_honey_type", data=data)
    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.INCONSISTANT_DATA


def test_create_new_honey_type_success(client):
    logged_in(client)

    data = {"name_fr": "test", "name_en": "te"}
    answer = client.post("/apiary/create/new_honey_type", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.NEW_PARAMETER_SUCCESS


def test_get_apiary_info_success(client):
    logged_in(client)

    data = {"ap_id": 1}
    answer = client.post("/apiary/get_apiary_info", data=data)
    assert answer.status_code == 200
    assert answer.json["id"] == 1


def test_get_apiary_info_fail(client):
    logged_in(client)

    data = {"ap_id": 2}  # wrong id

    answer = client.post("/apiary/get_apiary_info", data=data)
    assert answer.status_code == 500


def test_modify_apairy_success(client):
    logged_in(client)

    data = {
        "ap_id": 1,
        "name": "wesh",
        "location": "vazy",
        "status": 2,
        "honey": 3
    }
    answer = client.post("apiary/submit_apiary_info", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.MODIFICATION_SUCCESS

def test_modify_delete_apiary(client):
    logged_in(client)

    data = {"ap_id": 1}
    answer = client.post("apiary/delete", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.DELETION_SUCCESS







