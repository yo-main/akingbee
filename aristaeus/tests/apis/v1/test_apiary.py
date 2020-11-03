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


@pytest.mark.parametrize("name, location, status_id, honey_id, expected", (
    ("name", "location", uuid.uuid4(), uuid.uuid4(), 400),
    ("name", "location", IDS["Apiary_statuses"][0], uuid.uuid4(), 400),
    ("name", "location", uuid.uuid4(), IDS["Honey_types"][0], 400),
    ("name", "location", IDS["Apiary_statuses"][-1], IDS["Honey_types"][0], 400),
    ("name", "location", IDS["Apiary_statuses"][0], IDS["Honey_types"][-1], 400),
    ("", "location", IDS["Apiary_statuses"][0], IDS["Honey_types"][0], 422),
    ("name", "", IDS["Apiary_statuses"][0], IDS["Honey_types"][0], 422),
))
def test_post_apiary_fail(test_db, auth_token, test_app, name, location, status_id, honey_id, expected):
    data = {
        "name": name,
        "location": location,
        "status": str(status_id),
        "honey_type": str(honey_id),
    }

    if expected != 422:
        response = test_app.post("/apiary", json=data)
        assert response.status_code == 401

    response = test_app.post("/apiary", cookies={"access_token": auth_token}, json=data)
    assert response.status_code == expected