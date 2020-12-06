import pytest
import uuid

from gaea.rbmq import RBMQPublisher
from gaea.rbmq.utils.tests import MockRBMQConnectionManager
from gaea.models.utils.test import IDS

def test_get_apiary(test_db, auth_token, test_app):
    response = test_app.get("/apiary")
    assert response.status_code == 401

    response = test_app.get("/apiary", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize("name, location, honey_id, expected", (
    ("name", "location", uuid.uuid4(), 400),
    ("name", "location", IDS["Honey_types"][-1], 400),
    ("", "location", IDS["Honey_types"][0], 422),
    ("name", "", IDS["Honey_types"][0], 422),
))
def test_post_apiary_fail(test_db, auth_token, test_app, name, location, honey_id, expected):
    data = {
        "name": name,
        "location": location,
        "honey_type": str(honey_id),
    }

    if expected != 422:
        response = test_app.post("/apiary", json=data)
        assert response.status_code == 401

    response = test_app.post("/apiary", cookies={"access_token": auth_token}, json=data)
    assert response.status_code == expected

def test_post_apiary_and_delete(test_db, auth_token, test_app):
    data = {
        "name": "apiary",
        "location": "ici",
        "honey_type": str(IDS["Honey_types"][0]),
    }

    response = test_app.post("/apiary", cookies={"access_token": auth_token}, json=data)
    assert response.status_code == 200

    obj_id = response.json().get("id")
    assert obj_id

    response = test_app.get("/apiary", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 4

    response = test_app.delete(f"/apiary/{obj_id}", cookies={"access_token": auth_token})
    assert response.status_code == 204

    response = test_app.get("/apiary", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize("obj_id, data, expected", (
    (IDS["Apiaries"][0], {}, 400),
    (IDS["Apiaries"][0], {"name": "hop"}, 204),
    (uuid.uuid4(), {"name": "hop"}, 404),
))
def test_put_apiary(test_db, auth_token, test_app, obj_id, data, expected):
    response = test_app.put(f"/apiary/{str(obj_id)}", json=data)
    assert response.status_code == 401

    response = test_app.put(f"/apiary/{str(obj_id)}", cookies={"access_token": auth_token}, json=data)
    assert response.status_code == expected
