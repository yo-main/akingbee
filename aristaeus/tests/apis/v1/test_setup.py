import pytest

from gaea.rbmq import RBMQPublisher
from gaea.rbmq.utils.tests import MockRBMQConnectionManager

def test_swarm_health(test_db, auth_token, test_app):
    response = test_app.get("/setup/swarm_health_status", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = test_app.post("/setup/swarm_health_status", cookies={"access_token": auth_token}, json={"value": "coucou"})
    assert response.status_code == 200
    assert response.json().get("id")

    response = test_app.get("/setup/swarm_health_status", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 3
