import uuid
import pytest


def test_create_apiary(app):
    org_id = str(uuid.uuid4())
    data = {"name": "a name", "honey_kind": "too good", "location": "everywhere", "organization_id": org_id}
    response = app.post("/apiary", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == "a name", data
    assert data["location"] == "everywhere", data
    assert data["honey_kind"] == "too good", data
    assert data["organization_id"] == org_id, data


@pytest.mark.parametrize(
    "payload",
    (
        {"name": "a name", "honey_kind": "too good", "location": None, "organization_id": str(uuid.uuid4())},
        {"name": "a name", "honey_kind": "too good", "organization_id": str(uuid.uuid4())},
        {"location": "a name", "honey_kind": "too good", "organization_id": str(uuid.uuid4())},
        {"location": "a name", "name": "too good", "organization_id": str(uuid.uuid4())},
    ),
)
def test_create_apiary__wrong_payload(app, payload):
    response = app.post("/apiary", json=payload)
    assert response.status_code == 422, response.text


def test_get_apiary__unknown(app):
    response = app.get(f"/apiary/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


def test_get_apiary__get(app):
    data = {"name": "a name", "honey_kind": "too good", "location": "everywhere", "organization_id": str(uuid.uuid4())}
    response = app.post("/apiary", json=data)
    assert response.status_code == 200, response.text

    swarm_id = response.json()["public_id"]
    response = app.get(f"/apiary/{swarm_id}")
    assert response.status_code == 200, response.text
