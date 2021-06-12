import pytest
import uuid

from gaea.models.utils.test import IDS


def test_get_swarms(auth_token, test_app):
    response = test_app.get("/swarms")
    assert response.status_code == 401

    response = test_app.get("/swarms", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize(
    "swarm_health_id, year, expected",
    (
        (IDS["Swarm_health_statuses"][0], 2020, 200),
        (IDS["Swarm_health_statuses"][-1], 2021, 400),
        (uuid.uuid4(), 2019, 400),
        ("coucou", 2018, 422),
        (IDS["Swarm_health_statuses"][0], "coucou", 422),
        (IDS["Swarm_health_statuses"][0], None, 422),
    ),
)
def test_post_swarm(auth_token, test_app, swarm_health_id, year, expected):
    body = {"health_status_id": str(swarm_health_id), "queen_year": year}
    response = test_app.post("/swarm", json=body, cookies={"access_token": auth_token})
    assert response.status_code == expected


@pytest.mark.parametrize(
    "swarm_id, swarm_health_id, year, expected",
    (
        (IDS["Swarms"][0], IDS["Swarm_health_statuses"][0], None, 204),
        (IDS["Swarms"][-1], IDS["Swarm_health_statuses"][0], None, 404),
        (uuid.uuid4(), IDS["Swarm_health_statuses"][0], None, 404),
        (IDS["Swarms"][0], IDS["Swarm_health_statuses"][-1], None, 400),
        (IDS["Swarms"][0], uuid.uuid4(), None, 400),
        ("Hello", IDS["Swarm_health_statuses"][0], None, 422),
        (IDS["Swarms"][0], "Coucou", None, 422),
        (IDS["Swarms"][0], None, 1800, 204),
        (IDS["Swarms"][0], IDS["Swarm_health_statuses"][1], 1800, 204),
        (IDS["Swarms"][0], None, "coucou", 422),
        (IDS["Swarms"][0], None, None, 400),
    ),
)
def test_put_swarm(auth_token, test_app, swarm_id, swarm_health_id, year, expected):
    body = {"health_status_id": swarm_health_id, "queen_year": year}
    body = {k: str(v) for k, v in body.items() if v is not None}
    response = test_app.put(
        f"/swarm/{str(swarm_id)}", json=body, cookies={"access_token": auth_token}
    )
    assert response.status_code == expected


def test_delete_swarm(auth_token, test_app):
    swarm_body = {
        "health_status_id": str(IDS["Swarm_health_statuses"][0]),
        "queen_year": 1808,
    }
    response = test_app.post(
        "/swarm", json=swarm_body, cookies={"access_token": auth_token}
    )
    assert response.status_code == 200

    swarm_id = response.json()["id"]

    hive_body = {
        "name": "test",
        "condition_id": str(IDS["Hive_conditions"][0]),
        "owner_id": str(IDS["Owners"][0]),
        "swarm_id": swarm_id,
    }
    response = test_app.post(
        "/hive", json=hive_body, cookies={"access_token": auth_token}
    )
    assert response.status_code == 200

    hive_with_swarm = response.json()
    assert str(hive_with_swarm["swarm"]["id"]) == swarm_id

    response = test_app.delete(
        f"/swarm/{str(swarm_id)}", cookies={"access_token": auth_token}
    )
    assert response.status_code == 204

    response = test_app.get(
        f"/hive/{str(hive_with_swarm['id'])}", cookies={"access_token": auth_token}
    )
    assert response.status_code == 200

    hive_without_swarm = response.json()

    assert hive_without_swarm["swarm"] is None
