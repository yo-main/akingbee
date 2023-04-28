from datetime import datetime
from datetime import timezone

import pytest


@pytest.mark.parametrize("async_app", ["44444444-4444-4444-4444-444444444444"], indirect=True)
async def test_comment_endpoints(async_app):
    # CREATE HIVE
    data = {"name": "second hive name", "condition": "condition", "owner": "owner"}
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 201, response.text

    hive_id = response.json()["public_id"]

    # CREATE EVENT
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

    # POST
    data = {"body": "body", "date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(), "event_id": event_id}
    response = await async_app.post(f"/comment/{hive_id}", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["body"] == "body", data

    comment_id = data["public_id"]

    # GET
    response = await async_app.get(f"/comment/{comment_id}")
    assert response.status_code == 200, response.text
    assert response.json()["body"] == "body", response.text

    # UPDATE
    response = await async_app.put(f"/comment/{comment_id}", json={"body": "new body"})
    assert response.status_code == 200, response.text
    assert response.json()["body"] == "new body", response.text

    # LIST
    response = await async_app.get("/comment", params={"hive_id": hive_id})
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["body"] == "new body", response.text

    # DELETE
    response = await async_app.delete(f"/comment/{comment_id}")
    assert response.status_code == 204, response.text

    response = await async_app.get(f"/comment/{comment_id}")
    assert response.status_code == 404, response.text
