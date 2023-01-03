import uuid
from datetime import datetime, timezone

import pytest
from tests.factories import EventModelFactory, HiveModelFactory


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_event(async_app, session):
    public_id = str(uuid.uuid4())
    hive = HiveModelFactory.build(public_id=public_id)
    session.add(hive)
    await session.commit()
    data = {
        "title": "title",
        "description": "description",
        "due_date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "status": "status",
        "type": "type",
        "hive_id": public_id,
    }
    response = await async_app.post("/event", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["title"] == "title", data
    assert data["description"] == "description", data
    assert data["due_date"] == "2022-01-01T00:00:00", data
    assert data["status"] == "status", data
    assert data["type"] == "type", data
    assert data["hive_id"] == public_id, data


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
async def test_get_event(async_app, session):
    public_id = str(uuid.uuid4())
    hive = HiveModelFactory.build(public_id=public_id)
    session.add(hive)
    await session.commit()
    await session.refresh(hive)
    data = {
        "title": "title",
        "description": "description",
        "due_date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "status": "status",
        "type": "type",
        "hive_id": public_id,
    }
    response = await async_app.post("/event", json=data)
    assert response.status_code == 200, response.text

    event_id = response.json()["public_id"]
    response = await async_app.get(f"/event/{event_id}")
    assert response.status_code == 200, response.text


@pytest.mark.parametrize("async_app", ["33333333-3333-3333-3333-333333333333"], indirect=True)
async def test_list_events(async_app, session):
    hive_public_id = str(uuid.uuid4())
    hive = HiveModelFactory.build(
        organization_id="33333333-3333-3333-3333-333333333333", public_id=hive_public_id
    )
    session.add(hive)
    await session.commit()
    await session.refresh(hive)
    events = EventModelFactory.create_batch(5, hive_id=hive.id)
    session.add_all(events)
    await session.commit()

    response = await async_app.get("/event", params={"hive_id": hive_public_id})

    assert response.status_code == 200, response.text
    assert len(response.json()) == 5, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
@pytest.mark.parametrize(
    "payload",
    (
        {"title": "new title"},
        {"status": "new status"},
        {"description": "new description"},
        {"due_date": "2022-02-01T00:00:00"},
    ),
)
async def test_put_event__success(async_app, session, payload):
    hive = HiveModelFactory.build(organization_id="11111111-1111-1111-1111-111111111111")
    session.add(hive)
    await session.commit()
    await session.refresh(hive)
    event = EventModelFactory.create(hive_id=hive.id)
    session.add(event)
    await session.commit()
    await session.refresh(event)

    response = await async_app.put(f"/event/{event.public_id}", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in payload.items():
        assert data[key] == value


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_delete_hive__success(async_app, session):
    hive = HiveModelFactory.build(organization_id="11111111-1111-1111-1111-111111111111")
    session.add(hive)
    await session.commit()
    await session.refresh(hive)
    event = EventModelFactory.create(hive_id=hive.id)
    session.add(event)
    await session.commit()
    await session.refresh(event)

    response = await async_app.delete(f"/event/{event.public_id}")
    assert response.status_code == 204, response.text

    response = await async_app.get(f"/event/{event.public_id}")
    assert response.status_code == 404, response.text
