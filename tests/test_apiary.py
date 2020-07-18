# pylint: disable=redefined-outer-name,too-many-arguments,unused-import
import pytest

from tests.fixtures import client, fake_database, logged_in

from akb.constants import alert_codes
from akb.helpers.users import create_new_user


@pytest.fixture(scope="module", autouse=True)
def create_a_user(fake_database):
    create_new_user(
        {"username": "test", "pwd": "123azeAZE", "email": "aze@gmail.com"}
    )


@pytest.mark.parametrize(
    "name,location,honey,status,expected",
    [
        ("", "Location", "1", "1", 400),
        ("Name", "", "1", "1", 400),
        ("Name", "Location", "", "1", 400),
        ("Name", "Location", "1", "", 400),
        ("Name", "Location", "9", "1", 500),
        ("Name", "Location", "1", "5", 500),
    ],
)
def test_create_apiary_fail(name, location, honey, status, expected, client):
    logged_in(client)

    data = {
        "name": name,
        "location": location,
        "honey_type": honey,
        "status": status,
        "birthday": "01/01/2019",
    }
    answer = client.post("/api/apiary", data=data)
    assert answer.status_code == expected


def test_create_apiary_success(client):
    logged_in(client)

    data = {
        "name": "apiary",
        "location": "here",
        "honey_type": "1",
        "status": "1",
        "birthday": "01/01/2019",
    }
    answer = client.post("/api/apiary", data=data)
    assert answer.status_code == 200


def test_create_new_apiary_status_fail(client):
    logged_in(client)

    data = {"value": ""}
    answer = client.post("/api/apiary_status", data=data)
    assert answer.status_code == 400


def test_create_new_apiary_status_success(client):
    logged_in(client)

    data = {"value": "test"}
    answer = client.post("/api/apiary_status", data=data)
    assert answer.status_code == 200


def test_create_new_honey_type_fail(client):
    logged_in(client)

    data = {"value": ""}
    answer = client.post("/api/honey_type", data=data)
    assert answer.status_code == 400


def test_create_new_honey_type_success(client):
    logged_in(client)

    data = {"value": "test"}
    answer = client.post("/api/honey_type", data=data)
    assert answer.status_code == 200


def test_get_apiary_info_fail(client):
    logged_in(client)
    answer = client.get("/api/apiary/2")  # wrong id
    assert answer.status_code == 404


def test_get_apiary_info_success(client):
    logged_in(client)
    answer = client.get("/api/apiary/1")
    assert answer.status_code == 200
    assert answer.json["id"] == 1


@pytest.mark.parametrize(
    "ap_id,name,location,status,honey,expected",
    [
        (5, "name", "location", 1, 1, 404),
        (1, "", "location", 1, 1, 404),
        (1, "name", "", 1, 1, 404),
        (1, "name", "location", 9, 1, 404),
        (1, "name", "location", 1, 9, 404),
    ],
)
def test_modify_apiary_fail(
    client, expected, ap_id, name, location, status, honey
):
    logged_in(client)
    data = {
        "name": name,
        "location": location,
        "status": status,
        "honey": honey,
    }
    answer = client.put("/api/apiary/{ap_id}")
    assert answer.status_code == expected


def test_modify_apiary_success(client):
    logged_in(client)

    data = {"name": "wesh", "location": "vazy", "status": 2, "honey": 3}
    answer = client.put("/api/apiary/1", data=data)
    assert answer.status_code == 200


def test_modify_delete_apiary_fail(client):
    logged_in(client)
    answer = client.delete("/api/apiary/5")
    assert answer.status_code == 404


def test_modify_delete_apiary_success(client):
    logged_in(client)

    answer = client.delete("/api/apiary/1")
    assert answer.status_code == 200
