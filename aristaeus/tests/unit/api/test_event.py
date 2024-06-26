import uuid
from datetime import datetime
from datetime import timezone

import pytest
from aristaeus.domain.services.unit_of_work import UnitOfWork
from tests.factories import EventFactory
from tests.factories import HiveFactory


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_event(async_app):
    async with UnitOfWork() as uow:
        hive = HiveFactory.build()
        await uow.hive.save(hive)

    data = {
        "title": "title",
        "description": "description",
        "due_date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "status": "status",
        "type": "type",
        "hive_id": str(hive.public_id),
    }
    response = await async_app.post("/event", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["title"] == "title", data
    assert data["description"] == "description", data
    assert data["due_date"] == "2022-01-01T00:00:00", data
    assert data["status"] == "status", data
    assert data["type"] == "type", data
    assert data["hive"]["public_id"] == str(hive.public_id), data


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
    async with UnitOfWork() as uow:
        hive = HiveFactory.build()
        await uow.hive.save(hive)

    data = {
        "title": "title",
        "description": "description",
        "due_date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
        "status": "status",
        "type": "type",
        "hive_id": str(hive.public_id),
    }
    response = await async_app.post("/event", json=data)
    assert response.status_code == 200, response.text

    event_id = response.json()["public_id"]
    response = await async_app.get(f"/event/{event_id}")
    assert response.status_code == 200, response.text


@pytest.mark.parametrize("async_app", ["33333333-3333-3333-3333-333333333333"], indirect=True)
async def test_list_events(async_app):
    async with UnitOfWork() as uow:
        hive = HiveFactory.build(organization_id=uuid.UUID("33333333-3333-3333-3333-333333333333"))
        await uow.hive.save(hive)

        for event in EventFactory.create_batch(5, hive=hive):
            await uow.event.save(event)

    response = await async_app.get("/event", params={"hive_id": str(hive.public_id)})

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
async def test_put_event__success(async_app, payload):
    hive = HiveFactory.build(organization_id=uuid.UUID("11111111-1111-1111-1111-111111111111"))
    event = EventFactory.create(hive=hive)
    async with UnitOfWork() as uow:
        await uow.hive.save(hive)
        await uow.event.save(event)

    response = await async_app.put(f"/event/{event.public_id}", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in payload.items():
        assert data[key] == value


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_delete_hive__success(async_app):
    hive = HiveFactory.build(organization_id=uuid.UUID("11111111-1111-1111-1111-111111111111"))
    event = EventFactory.create(hive=hive)
    async with UnitOfWork() as uow:
        await uow.hive.save(hive)
        await uow.event.save(event)

    response = await async_app.delete(f"/event/{event.public_id}")
    assert response.status_code == 204, response.text

    response = await async_app.get(f"/event/{event.public_id}")
    assert response.status_code == 404, response.text
