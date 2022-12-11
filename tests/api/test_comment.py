import uuid
import pytest
from datetime import datetime
from datetime import timezone


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_comment(async_app):
    hive_id = str(uuid.uuid4())
    data = {
        "type": "type",
        "body": "body",
        "date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "type": "type",
        "hive_id": hive_id,
    }
    response = await async_app.post("/comment", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["type"] == "type", data
    assert data["body"] == "body", data
    assert data["date"] == "2022-01-01T00:00:00", data
    assert data["type"] == "type", data
    assert data["hive_id"] == hive_id, data


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
@pytest.mark.parametrize(
    "payload",
    (
        {"type": None},
        {"body": None},
        {"type": None},
        {"hive_id": None},
        {"date": None},
        {"date": "i_am_not_a_date"},
        {"hive_id": "i_am_not_a_uuid"},
    ),
)
async def test_create_comment__wrong_payload(async_app, payload):
    data = {
        "type": "type",
        "body": "description",
        "date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "type": "type",
        "hive_id": str(uuid.uuid4()),
    }
    data.update(payload)
    data = {k: v for k, v in data.items() if v is not None}
    response = await async_app.post("/comment", json=data)
    assert response.status_code == 422, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_comment__unknown(async_app):
    response = await async_app.get(f"/comment/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_comment(async_app):
    hive_id = str(uuid.uuid4())
    data = {
        "type": "type",
        "body": "description",
        "date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "type": "type",
        "hive_id": hive_id,
    }
    response = await async_app.post("/comment", json=data)
    assert response.status_code == 200, response.text

    comment_id = response.json()["public_id"]
    response = await async_app.get(f"/comment/{comment_id}")
    assert response.status_code == 200, response.text
