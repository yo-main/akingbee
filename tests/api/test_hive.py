import uuid
import pytest

from tests.factories import HiveModelFactory


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_hive__no_apiary(async_app):
    owner_id = str(uuid.uuid4())
    data = {"name": "a name", "condition": "too good", "owner_id": owner_id}
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == "a name", data
    assert data["condition"] == "too good", data
    assert data["owner_id"] == owner_id, data
    assert data["apiary_id"] is None, data
    assert data["organization_id"] == "11111111-1111-1111-1111-111111111111", data


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_hive__with_apiary(async_app):
    owner_id = str(uuid.uuid4())
    apiary_id = str(uuid.uuid4())
    data = {
        "name": "a name",
        "condition": "too good",
        "owner_id": owner_id,
        "apiary_id": apiary_id,
    }
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == "a name", data
    assert data["condition"] == "too good", data
    assert data["owner_id"] == owner_id, data
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
            "owner_id": "coucou",
        },
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
    owner_id = str(uuid.uuid4())
    apiary_id = str(uuid.uuid4())

    data = {
        "name": "a name",
        "condition": "too good",
        "owner_id": owner_id,
        "apiary_id": apiary_id,
    }
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 200, response.text

    hive_id = response.json()["public_id"]
    response = await async_app.get(f"/hive/{hive_id}")
    assert response.status_code == 200, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_hive__no_apiary(async_app):
    owner_id = str(uuid.uuid4())

    data = {"name": "a name", "condition": "too good", "owner_id": owner_id}
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 200, response.text

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
