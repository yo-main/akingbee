import pytest
import uuid

from gaea.rbmq import RBMQPublisher
from gaea.rbmq.utils.tests import MockRBMQConnectionManager
from gaea.models.utils.test import IDS

def test_get_hives(auth_token, test_app):
    response = test_app.get("/hive")
    assert response.status_code == 401

    response = test_app.get("/hive", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize("data, expected", (
    ({}, 400),
    ({"condition_id": "no-uuid"}, 422),
    ({"owner_id": "no-uuid"}, 422),
    ({"apiary_id": "no-uuid"}, 422),
    ({"swarm_id": "no-uuid"}, 422),
    ({"owner_id": None}, 422),
    ({"condition_id": None}, 422),
    ({"owner_id": IDS["Owners"][-1]}, 400),
    ({"condition_id": IDS["Hive_conditions"][-1]}, 400),
    ({"apiary_id": IDS["Apiaries"][-1]}, 400),
    ({"swarm_id": IDS["Swarms"][-1]}, 400),
    ({"apiary_id": IDS["Apiaries"][0], "swarm_id": IDS["Swarms"][-1]}, 400),
    ({"apiary_id": IDS["Apiaries"][-1], "swarm_id": IDS["Swarms"][0]}, 400),
))
def test_post_hive_fail(auth_token, test_app, data, expected):
    body = {
        "name": "name",
        "condition_id": uuid.uuid4(),
        "owner_id": uuid.uuid4(),
        "swarm_id": None,
        "apiary_id": None,
    }
    body.update(data)
    body = {k:str(v) for k, v in body.items() if v is not None}

    if expected != 422:
        response = test_app.post("/hive", json=body)
        assert response.status_code == 401

    response = test_app.post("/hive", cookies={"access_token": auth_token}, json=body)
    assert response.status_code == expected

@pytest.mark.parametrize("data", (
    {},
    {"swarm_id": IDS["Swarms"][0]},
    {"apiary_id": IDS["Apiaries"][0]},
    {"apiary_id": IDS["Apiaries"][1], "swarm_id": IDS["Swarms"][1]},
))
def test_post_hive_and_delete(auth_token, test_app, data):
    body = {
        "name": "name",
        "condition_id": IDS["Hive_conditions"][0],
        "owner_id": IDS["Owners"][0],
        "swarm_id": None,
        "apiary_id": None,
    }
    body.update(data)
    body = {k:str(v) for k, v in body.items() if v is not None}

    response = test_app.post("/hive", cookies={"access_token": auth_token}, json=body)
    assert response.status_code == 200

    obj_id = response.json().get("id")
    assert obj_id

    response = test_app.get("/hive", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 4

    response = test_app.delete(f"/hive/{obj_id}", cookies={"access_token": auth_token})
    assert response.status_code == 204

    response = test_app.get("/hive", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = test_app.get(f"/hive/{obj_id}", cookies={"access_token": auth_token})
    assert response.status_code == 404

    response = test_app.delete(f"/hive/{obj_id}", cookies={"access_token": auth_token})
    assert response.status_code == 404


@pytest.mark.parametrize("hive_id, data, expected", (
    (IDS["Hives"][0], {}, 400),
    (IDS["Hives"][0], {"name": "hop"}, 204),
    (IDS["Hives"][0], {"owner_id": IDS["Owners"][1]}, 204),
    (IDS["Hives"][0], {"owner_id": IDS["Owners"][-1]}, 400),
    (uuid.uuid4(), {"name": "hop"}, 404),
    (IDS["Hives"][-1], {"name": "hop"}, 404),
))
def test_put_hive(auth_token, test_app, hive_id, data, expected):
    data = {k: str(v) for k, v in data.items()}
    response = test_app.put(f"/hive/{str(hive_id)}", json=data)
    assert response.status_code == 401

    response = test_app.put(f"/hive/{str(hive_id)}", cookies={"access_token": auth_token}, json=data)
    assert response.status_code == expected

@pytest.mark.parametrize("hive_id, expected", (
    (IDS["Hives"][0], 200),
    (IDS["Hives"][-1], 404),
    (uuid.uuid4(), 404),
    ("random", 422),
    ("123", 422),
    (None, 422),
))
def test_get_hive(auth_token, test_app, hive_id, expected):
    response = test_app.get(f"/hive/{str(hive_id)}", cookies={"access_token": auth_token})
    assert response.status_code == expected


@pytest.mark.parametrize("hive_id, apiary_id, expected", (
    (IDS["Hives"][0], IDS["Apiaries"][1], 204),
    (IDS["Hives"][0], IDS["Apiaries"][0], 204),
    (IDS["Hives"][-1], IDS["Apiaries"][0], 404),
    (IDS["Hives"][0], IDS["Apiaries"][-1], 404),
    (uuid.uuid4(), IDS["Apiaries"][-1], 404),
    (IDS["Hives"][0], uuid.uuid4(), 404),
))
def test_move_hive(auth_token, test_app, hive_id, apiary_id, expected):
    response = test_app.put(f"/hive/{str(hive_id)}/move/{str(apiary_id)}", cookies={"access_token": auth_token})
    assert response.status_code == expected

