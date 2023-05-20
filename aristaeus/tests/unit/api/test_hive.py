import uuid

import pytest
from tests.factories import ApiaryFactory
from tests.factories import HiveFactory
from tests.factories import SwarmFactory

from aristaeus.domain.services.unit_of_work import UnitOfWork


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_hive__no_apiary(async_app):
    data = {"name": "a name", "condition": "too good", "owner": "owner"}
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 201, response.text

    data = response.json()
    assert data["name"] == "a name", data
    assert data["condition"] == "too good", data
    assert data["owner"] == "owner", data
    assert data["apiary"] is None, data
    assert data["organization_id"] == "11111111-1111-1111-1111-111111111111", data


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_hive__with_apiary(async_app):
    apiary = ApiaryFactory.create()
    async with UnitOfWork() as uow:
        await uow.apiary.save(apiary)
        await uow.commit()

    data = {
        "name": "a name",
        "condition": "too good",
        "owner": "owner",
        "apiary_id": str(apiary.public_id),
    }
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 201, response.text

    data = response.json()
    assert data["name"] == "a name", data
    assert data["condition"] == "too good", data
    assert data["owner"] == "owner", data
    assert data["apiary"]["public_id"] == str(apiary.public_id), data
    assert data["organization_id"] == "11111111-1111-1111-1111-111111111111", data


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
@pytest.mark.parametrize(
    "payload",
    (
        {"name": "a name"},
        {"name": "a name", "condition": "too good"},
        {
            "name": "a name",
            "condition": "too good",
            "apiary_id": "coucou",
        },
    ),
)
async def test_create_hive__wrong_payload(async_app, payload):
    response = await async_app.post("/hive", json=payload)
    assert response.status_code == 422, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_hive__unknown(async_app):
    response = await async_app.get(f"/hive/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_hive__with_apiary(async_app):
    apiary = ApiaryFactory.create()
    async with UnitOfWork() as uow:
        await uow.apiary.save(apiary)
        await uow.commit()

    data = {
        "name": "a name",
        "condition": "too good",
        "owner": "owner",
        "apiary_id": str(apiary.public_id),
    }
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 201, response.text

    hive_id = response.json()["public_id"]
    response = await async_app.get(f"/hive/{hive_id}")
    assert response.status_code == 200, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_hive__no_apiary(async_app):
    data = {"name": "a name", "condition": "too good", "owner": "owner"}
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 201, response.text

    hive_id = response.json()["public_id"]
    response = await async_app.get(f"/hive/{hive_id}")
    assert response.status_code == 200, response.text


@pytest.mark.parametrize("async_app", ["22222222-2222-2222-2222-222222222222"], indirect=True)
async def test_list_hives(async_app):
    apiary = ApiaryFactory.build(organization_id=uuid.UUID("22222222-2222-2222-2222-222222222222"), name="apiary_name")
    swarms = SwarmFactory.create_batch(5, queen_year=2000)
    hives = [
        HiveFactory.create(
            organization_id=uuid.UUID("22222222-2222-2222-2222-222222222222"), apiary=apiary, swarm=swarm
        )
        for swarm in swarms
    ]
    async with UnitOfWork() as uow:
        await uow.apiary.save(apiary)
        for swarm in swarms:
            await uow.swarm.save(swarm)
        for hive in hives:
            await uow.hive.save(hive)
        await uow.commit()

    response = await async_app.get("/hive")

    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 5, response.text
    assert data[0]["apiary"]["name"] == "apiary_name"
    assert data[0]["swarm"]["queen_year"] == 2000


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
@pytest.mark.parametrize(
    "payload",
    (
        {"condition": "new condition"},
        {"name": "new name"},
        {"owner": "owner"},
    ),
)
async def test_put_hive__success(async_app, payload):
    apiary = ApiaryFactory.create()
    hive = HiveFactory.create()
    async with UnitOfWork() as uow:
        await uow.apiary.save(apiary)
        await uow.hive.save(hive)
        await uow.commit()

    data = {
        "name": "a name",
        "condition": "too good",
        "apiary_id": str(apiary.public_id),
        "owner": "owner",
    }

    response = await async_app.put(f"/hive/{hive.public_id}", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in payload.items():
        assert data[key] == value


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_delete_hive__success(async_app):
    hive = HiveFactory.create()
    async with UnitOfWork() as uow:
        await uow.hive.save(hive)

    response = await async_app.delete(f"/hive/{hive.public_id}")
    assert response.status_code == 204, response.text

    response = await async_app.get(f"/hive/{hive.public_id}")
    assert response.status_code == 404, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_move_hive(async_app):
    apiary = ApiaryFactory.create(organization_id=uuid.UUID("11111111-1111-1111-1111-111111111111"))
    hive = HiveFactory.create(organization_id=apiary.organization_id)
    async with UnitOfWork() as uow:
        await uow.apiary.save(apiary)
        await uow.hive.save(hive)
        await uow.commit()

    response = await async_app.put(f"/hive/{hive.public_id}/move/{apiary.public_id}")
    assert response.status_code == 200, response.text
    assert response.json()["public_id"] == str(hive.public_id)
    assert response.json()["apiary"]["public_id"] == str(apiary.public_id)