import uuid
import pytest


def test_create_apiary(app):
    data = {"name": "a name", "honey_kind": "too good", "location": "everywhere"}
    response = app.post("/apiary", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == "a name", data
    assert data["location"] == "everywhere", data
    assert data["honey_kind"] == "too good", data
    assert data["organization_id"] == "11111111-1111-1111-1111-111111111111", data


@pytest.mark.parametrize(
    "payload",
    (
        {"name": "a name", "honey_kind": "too good", "location": None},
        {"name": "a name", "honey_kind": "too good"},
        {"location": "a name", "honey_kind": "too good"},
        {"location": "a name", "name": "too good"},
    ),
)
def test_create_apiary__wrong_payload(app, payload):
    response = app.post("/apiary", json=payload)
    assert response.status_code == 422, response.text


def test_get_apiary__unknown(app):
    response = app.get(f"/apiary/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


def test_get_apiary__get(app):
    data = {"name": "a name", "honey_kind": "too good", "location": "everywhere"}
    response = app.post("/apiary", json=data)
    assert response.status_code == 200, response.text

    swarm_id = response.json()["public_id"]
    response = app.get(f"/apiary/{swarm_id}")
    assert response.status_code == 200, response.text
