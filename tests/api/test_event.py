import uuid
import pytest
from datetime import datetime
from datetime import timezone


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_event(async_app):
    hive_id = str(uuid.uuid4())
    data = {
        "title": "title",
        "description": "description",
        "due_date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "status": "status",
        "type": "type",
        "hive_id": hive_id,
    }
    response = await async_app.post("/event", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["title"] == "title", data
    assert data["description"] == "description", data
    assert data["due_date"] == "2022-01-01T00:00:00", data
    assert data["status"] == "status", data
    assert data["type"] == "type", data
    assert data["hive_id"] == hive_id, data


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
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
async def test_create_event__wrong_payload(async_app, payload):
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
    response = await async_app.post("/event", json=data)
    assert response.status_code == 422, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_event__unknown(async_app):
    response = await async_app.get(f"/event/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_event(async_app):
    hive_id = str(uuid.uuid4())
    data = {
        "title": "title",
        "description": "description",
        "due_date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "status": "status",
        "type": "type",
        "hive_id": hive_id,
    }
    response = await async_app.post("/event", json=data)
    assert response.status_code == 200, response.text

    event_id = response.json()["public_id"]
    response = await async_app.get(f"/event/{event_id}")
    assert response.status_code == 200, response.text
