import uuid

import pytest
from tests.factories import ApiaryModelFactory, HiveModelFactory


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_hive__no_apiary(async_app):
    data = {"name": "a name", "condition": "too good", "owner": "owner"}
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 201, response.text

    data = response.json()
    assert data["name"] == "a name", data
    assert data["condition"] == "too good", data
    assert data["owner"] == "owner", data
    assert data["apiary_id"] is None, data
    assert data["organization_id"] == "11111111-1111-1111-1111-111111111111", data


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_hive__with_apiary(async_app):
    apiary_id = str(uuid.uuid4())
    data = {
        "name": "a name",
        "condition": "too good",
        "owner": "owner",
        "apiary_id": apiary_id,
    }
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 201, response.text

    data = response.json()
    assert data["name"] == "a name", data
    assert data["condition"] == "too good", data
    assert data["owner"] == "owner", data
    assert data["apiary_id"] == apiary_id, data
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
    apiary_id = str(uuid.uuid4())

    data = {
        "name": "a name",
        "condition": "too good",
        "owner": "owner",
        "apiary_id": apiary_id,
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
async def test_list_hives(async_app, session):
    hives = HiveModelFactory.build_batch(5, organization_id="22222222-2222-2222-2222-222222222222")
    session.add_all(hives)
    await session.commit()

    response = await async_app.get("/hive")

    assert response.status_code == 200, response.text
    assert len(response.json()) == 5, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
@pytest.mark.parametrize(
    "payload",
    (
        {"condition": "new condition"},
        {"name": "new name"},
        {"owner": "owner"},
    ),
)
async def test_put_hive__success(async_app, session, payload):
    apiary = ApiaryModelFactory.create()
    session.add(apiary)
    await session.commit()
    await session.refresh(apiary)

    data = {
        "name": "a name",
        "condition": "too good",
        "apiary_id": str(apiary.public_id),
        "owner": "owner",
    }
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 201, response.text
    hive_id = response.json()["public_id"]

    response = await async_app.put(f"/hive/{hive_id}", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in payload.items():
        assert data[key] == value


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_delete_hive__success(async_app):
    data = {"name": "a name", "condition": "too good", "owner": "owner"}
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 201, response.text
    hive_id = response.json()["public_id"]

    response = await async_app.delete(f"/hive/{hive_id}")
    assert response.status_code == 204, response.text

    response = await async_app.get(f"/hive/{hive_id}")
    assert response.status_code == 404, response.text
