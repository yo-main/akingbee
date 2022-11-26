import uuid
import pytest


def test_create_hive__no_apiary(app):
    owner_id = str(uuid.uuid4())
    org_id = str(uuid.uuid4())
    data = {"name": "a name", "condition": "too good", "owner_id": owner_id, "organization_id": org_id}
    response = app.post("/hive", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == "a name", data
    assert data["condition"] == "too good", data
    assert data["owner_id"] == owner_id, data
    assert data["apiary_id"] == None, data
    assert data["organization_id"] == org_id, data


def test_create_hive__with_apiary(app):
    owner_id = str(uuid.uuid4())
    apiary_id = str(uuid.uuid4())
    org_id = str(uuid.uuid4())
    data = {
        "name": "a name",
        "condition": "too good",
        "owner_id": owner_id,
        "apiary_id": apiary_id,
        "organization_id": org_id,
    }
    response = app.post("/hive", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == "a name", data
    assert data["condition"] == "too good", data
    assert data["owner_id"] == owner_id, data
    assert data["apiary_id"] == apiary_id, data
    assert data["organization_id"] == org_id, data


@pytest.mark.parametrize(
    "payload",
    (
        {"name": "a name", "organization_id": str(uuid.uuid4())},
        {"name": "a name", "condition": "too good", "organization_id": str(uuid.uuid4())},
        {
            "name": "a name",
            "condition": "too good",
            "owner_id": "coucou",
            "organization_id": str(uuid.uuid4()),
            "organization_id": str(uuid.uuid4()),
        },
        {
            "name": "a name",
            "condition": "too good",
            "apiary_id": "coucou",
            "organization_id": str(uuid.uuid4()),
            "organization_id": str(uuid.uuid4()),
        },
    ),
)
def test_create_hive__wrong_payload(app, payload):
    response = app.post("/hive", json=payload)
    assert response.status_code == 422, response.text


def test_get_hive__unknown(app):
    response = app.get(f"/hive/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


def test_get_hive__with_apiary(app):
    owner_id = str(uuid.uuid4())
    apiary_id = str(uuid.uuid4())
    org_id = str(uuid.uuid4())

    data = {
        "name": "a name",
        "condition": "too good",
        "owner_id": owner_id,
        "apiary_id": apiary_id,
        "organization_id": org_id,
    }
    response = app.post("/hive", json=data)
    assert response.status_code == 200, response.text

    hive_id = response.json()["public_id"]
    response = app.get(f"/hive/{hive_id}")
    assert response.status_code == 200, response.text


def test_get_hive__no_apiary(app):
    owner_id = str(uuid.uuid4())
    org_id = str(uuid.uuid4())

    data = {"name": "a name", "condition": "too good", "owner_id": owner_id, "organization_id": org_id}
    response = app.post("/hive", json=data)
    assert response.status_code == 200, response.text

    hive_id = response.json()["public_id"]
    response = app.get(f"/hive/{hive_id}")
    assert response.status_code == 200, response.text
