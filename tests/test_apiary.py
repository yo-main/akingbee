# pylint: disable=redefined-outer-name,too-many-arguments,unused-import
import pytest

from tests.fixtures import client, fake_database, logged_in

from src.constants import alert_codes
from src.helpers.users import create_new_user


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
    answer = client.post("/apiary", data=data)
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
    answer = client.post("/apiary", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.NEW_APIARY_SUCCESS


def test_create_new_apiary_status_fail(client):
    logged_in(client)

    data = {"value": ""}
    answer = client.post("/apiary_status", data=data)
    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.INCONSISTANT_DATA


def test_create_new_apiary_status_success(client):
    logged_in(client)

    data = {"value": "test"}
    answer = client.post("/apiary_status", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.NEW_PARAMETER_SUCCESS


def test_create_new_honey_type_fail(client):
    logged_in(client)

    data = {"value": ""}
    answer = client.post("/honey_type", data=data)
    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.INCONSISTANT_DATA


def test_create_new_honey_type_success(client):
    logged_in(client)

    data = {"value": "test"}
    answer = client.post("/honey_type", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.NEW_PARAMETER_SUCCESS


def test_get_apiary_info_fail(client):
    logged_in(client)
    answer = client.get("/apiary/2") # wrong id
    assert answer.status_code == 500


def test_get_apiary_info_success(client):
    logged_in(client)
    answer = client.get("/apiary/1")
    assert answer.status_code == 200
    assert answer.json["id"] == 1


@pytest.mark.parametrize("ap_id,name,location,status,honey,expected", [
    (5, "name", "location", 1, 1, 500),
    (1, "", "location", 1, 1, 500),
    (1, "name", "", 1, 1, 500),
    (1, "name", "location", 9, 1, 500),
    (1, "name", "location", 1, 9, 500),
])
def test_modify_apiary_fail(client, expected, ap_id, name, location, status, honey):
    logged_in(client)
    data = {
        "name": name,
        "location": location,
        "status": status,
        "honey": honey
    }
    answer = client.put("/apiary/{ap_id}")
    assert answer.status_code == expected


def test_modify_apiary_success(client):
    logged_in(client)

    data = {
        "name": "wesh",
        "location": "vazy",
        "status": 2,
        "honey": 3
    }
    answer = client.put("/apiary/1", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.MODIFICATION_SUCCESS


def test_modify_delete_apiary_fail(client):
    logged_in(client)
    answer = client.delete("/apiary/5")
    assert answer.status_code == 500


def test_modify_delete_apiary_success(client):
    logged_in(client)

    answer = client.delete("/apiary/1")
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.DELETION_SUCCESS
