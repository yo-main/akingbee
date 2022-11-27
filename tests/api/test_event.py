import uuid
import pytest
from datetime import datetime
from datetime import timezone


def test_create_event(app):
    hive_id = str(uuid.uuid4())
    data = {
        "title": "title",
        "description": "description",
        "due_date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "status": "status",
        "type": "type",
        "hive_id": hive_id,
    }
    response = app.post("/event", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["title"] == "title", data
    assert data["description"] == "description", data
    assert data["due_date"] == "2022-01-01T00:00:00", data
    assert data["status"] == "status", data
    assert data["type"] == "type", data
    assert data["hive_id"] == hive_id, data


@pytest.mark.parametrize(
    "payload",
    (
        {"title": None},
        {"description": None},
        {"status": None},
        {"type": None},
        {"hive_id": None},
        {"due_date": None},
        {"due_date": "i_am_not_a_date"},
        {"hive_id": "i_am_not_a_uuid"},
    ),
)
def test_create_event__wrong_payload(app, payload):
    data = {
        "title": "title",
        "description": "description",
        "due_date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "status": "status",
        "type": "type",
        "hive_id": str(uuid.uuid4()),
    }
    data.update(payload)
    data = {k: v for k, v in data.items() if v is not None}
    response = app.post("/event", json=data)
    assert response.status_code == 422, response.text


def test_get_event__unknown(app):
    response = app.get(f"/event/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


def test_get_event(app):
    hive_id = str(uuid.uuid4())
    data = {
        "title": "title",
        "description": "description",
        "due_date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "status": "status",
        "type": "type",
        "hive_id": hive_id,
    }
    response = app.post("/event", json=data)
    assert response.status_code == 200, response.text

    event_id = response.json()["public_id"]
    response = app.get(f"/event/{event_id}")
    assert response.status_code == 200, response.text
