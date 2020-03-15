import datetime

import pytest

from tests.fixtures import client, fake_database, logged_in

from common.models import Apiary, Hive, CommentType

from webapp.constants import alert_codes as alerts
from webapp.helpers.users import create_new_user


@pytest.fixture(scope="module", autouse=True)
def setup_database(fake_database):
    create_new_user(
        {"username": "test", "pwd": "123azeAZE", "email": "aze@gmail.com"}
    )

    CommentType(en="english", fr="french").save()
    CommentType(en="french", fr="english").save()

    Apiary(
        user_id=1,
        name="tets_apiary",
        status=1,
        birthday=datetime.date.today(),
        location="test_location",
        honey_type=1,
    ).save()

    Apiary(
        user_id=1,
        name="here",
        status=1,
        birthday=datetime.date.today(),
        location="there",
        honey_type=2,
    ).save()

    Hive(
        user_id=1,
        name="my_hive",
        owner=1,
        apiary=1,
        condition=1,
        birthday=datetime.datetime.now(),
    )


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


@pytest.mark.parametrize(
    "name,birthday,apiary,owner,condition,expected",
    [
        ("", "19/12/2019", 1, 1, 1, 500),
        ("name", "12/19/2019", 1, 1, 1, 400),
        ("name", "19/12/2019", 9, 1, 1, 500),
        ("name", "19/12/2019", 1, 9, 1, 500),
        ("name", "19/12/2019", 1, 1, 9, 500),
    ],
)
def test_create_new_hive_fail(
    name, birthday, apiary, owner, condition, client, expected
):
    logged_in(client)

    data = {
        "name": name,
        "date": birthday,
        "apiary": apiary,
        "owner": owner,
        "hive_condition": condition,
    }
    answer = client.post("/api/hive", data=data)
    assert answer.status_code == expected


def test_create_new_hive_success(client):
    logged_in(client)

    data = {
        "name": "test_hive",
        "date": "19/12/2019",
        "apiary": 1,
        "owner": 1,
        "hive_condition": 1,
    }
    answer = client.post("/api/hive", data=data)
    assert answer.status_code == 200


def test_get_hive_info_fail(client):
    logged_in(client)
    answer = client.get("/api/hive/10")
    assert answer.status_code == 404


def test_get_hive_info_success(client):
    logged_in(client)
    answer = client.get("/api/hive/1")
    assert answer.status_code == 200
    assert answer.json["id"] == 1


@pytest.mark.parametrize(
    "hive_id,name,owner,expected",
    [(1, "", 1, 400), (1, 1, 10, 500), (10, 1, 1, 404)],
)
def test_modify_hive_fail(hive_id, name, owner, expected, client):
    logged_in(client)

    data = {"hive": name, "owner": owner}
    answer = client.put(f"/api/hive/{hive_id}", data=data)
    assert answer.status_code == expected


def test_modify_hive_success(client):
    logged_in(client)

    data = {"hive": "test_hive_modification", "apiary": 1, "owner": 1}
    answer = client.put("/api/hive/1", data=data)
    assert answer.status_code == 200


def test_move_hive_success(client):
    logged_in(client)

    assert Hive.get_by_id(1).apiary_id == 1
    answer = client.post("/api/hive/1/move/2")
    assert answer.status_code == 200
    assert Hive.get_by_id(1).apiary_id == 2
    answer = client.post("/api/hive/1/move/1")
    assert Hive.get_by_id(1).apiary_id == 1


def test_move_hive_fail(client):
    logged_in(client)

    assert Hive.get_by_id(1).apiary_id == 1
    answer = client.post("/api/hive/1/move/3")
    assert answer.status_code == 404


def test_add_swarm_success(client):
    logged_in(client)
    data = {"hive_id": 1, "swarm_health": 1}

    assert Hive.get_by_id(1).swarm == None
    answer = client.post("/api/swarm", data=data)
    assert answer.status_code == 200


@pytest.mark.parametrize("swarm_health, hive_id", ((9, 1), (1, 8)))
def test_add_swarm_fail(client, swarm_health, hive_id):
    logged_in(client)
    data = {"hive_id": hive_id, "swarm_health": swarm_health}

    answer = client.post("/api/swarm", data=data)
    assert answer.status_code == 400


def test_delete_swarm_success(client):
    logged_in(client)
    data = {"hive_id": 1}

    assert Hive.get_by_id(1).swarm_id == 1
    answer = client.delete("/api/swarm", data=data)
    assert answer.status_code == 200
