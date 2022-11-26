import uuid
import pytest


def test_create_swarm(app):
    data = {"queen_year": 2020, "health": "Good"}
    response = app.post("/swarm", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["queen_year"] == 2020, data
    assert data["health"] == "Good", data


@pytest.mark.parametrize(
    "payload",
    (
        {"health": "Good"},
        {"queen_year": "Good"},
        {"health": "Ok", "queen_year": None},
        {"health": "Ok", "queen_year": ""},
        {"health": "", "queen_year": "bla"},
    ),
)
def test_create_swarm__wrong_payload(app, payload):
    response = app.post("/swarm", json=payload)
    assert response.status_code == 422, response.text


def test_get_swarm__unknown(app):
    response = app.get(f"/swarm/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


def test_get_swarm__get(app):
    data = {"queen_year": 2010, "health": "Ok"}
    response = app.post("/swarm", json=data)
    assert response.status_code == 200, response.text

    swarm_id = response.json()["public_id"]
    response = app.get(f"/swarm/{swarm_id}")
    assert response.status_code == 200, response.text
