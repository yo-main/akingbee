import pytest
import uuid

from gaea.models.utils.test import IDS

def test_get_swarms(auth_token, test_app):
    response = test_app.get("/swarms")
    assert response.status_code == 401

    response = test_app.get("/swarms", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 3

@pytest.mark.parametrize("swarm_health_id, expected", (
    (IDS["Swarm_health_statuses"][0], 200),
    (IDS["Swarm_health_statuses"][-1], 400),
    (uuid.uuid4(), 400),
    ("coucou", 422),
))
def test_post_swarm(auth_token, test_app, swarm_health_id, expected):
    body = {"health_status_id": str(swarm_health_id)}
    response = test_app.post("/swarm", json=body, cookies={"access_token": auth_token})
    assert response.status_code == expected

@pytest.mark.parametrize("swarm_id, swarm_health_id, expected", (
    (IDS["Swarms"][0], IDS["Swarm_health_statuses"][0], 204),
    (IDS["Swarms"][-1], IDS["Swarm_health_statuses"][0], 404),
    (uuid.uuid4(), IDS["Swarm_health_statuses"][0], 404),
    (IDS["Swarms"][0], IDS["Swarm_health_statuses"][-1], 400),
    (IDS["Swarms"][0], uuid.uuid4(), 400),
    ("Hello", IDS["Swarm_health_statuses"][0], 422),
    (IDS["Swarms"][0], "Coucou", 422),
))
def test_put_swarm(auth_token, test_app, swarm_id, swarm_health_id, expected):
    body = {"health_status_id": str(swarm_health_id)}
    response = test_app.put(f"/swarm/{str(swarm_id)}", json=body, cookies={"access_token": auth_token})
    assert response.status_code == expected

