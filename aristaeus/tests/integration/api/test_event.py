from datetime import datetime
from datetime import timezone

import pytest


@pytest.mark.parametrize("async_app", ["55555555-5555-5555-5555-555555555555"], indirect=True)
async def test_event_endpoints(async_app):
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

    data = response.json()
    assert data["title"] == "title", response.text

    event_id = data["public_id"]

    # GET
    response = await async_app.get(f"/event/{event_id}")
    assert response.status_code == 200, response.text
    assert response.json()["title"] == "title", response.text

    # UPDATE
    response = await async_app.put(f"/event/{event_id}", json={"title": "new title"})
    assert response.status_code == 200, response.text
    assert response.json()["title"] == "new title", response.text

    # LIST
    response = await async_app.get("/event", params={"hive_id": hive_id})
    assert response.status_code == 200, response.text

    data = response.json()
    assert len(data) == 1, data
    assert data[0]["title"] == "new title", data

    # DELETE
    response = await async_app.delete(f"/event/{event_id}")
    assert response.status_code == 204, response.text
    response = await async_app.get(f"/event/{event_id}")
    assert response.status_code == 404, response.text
