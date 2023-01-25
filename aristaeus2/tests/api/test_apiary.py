import uuid
import pytest

from tests.factories import ApiaryModelFactory, HiveModelFactory


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_apiary(async_app):
    data = {"name": "a name", "honey_kind": "too good", "location": "everywhere"}
    response = await async_app.post("/apiary", json=data)
    assert response.status_code == 201, response.text

    data = response.json()
    assert data["name"] == "a name", data
    assert data["location"] == "everywhere", data
    assert data["honey_kind"] == "too good", data
    assert data["organization_id"] == "11111111-1111-1111-1111-111111111111", data


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
@pytest.mark.parametrize(
    "payload",
    (
        {"name": "a name", "honey_kind": "too good", "location": None},
        {"name": "a name", "honey_kind": "too good"},
        {"location": "a name", "honey_kind": "too good"},
        {"location": "a name", "name": "too good"},
    ),
)
async def test_create_apiary__wrong_payload(async_app, payload):
    response = await async_app.post("/apiary", json=payload)
    assert response.status_code == 422, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_apiary__unknown(async_app):
    response = await async_app.get(f"/apiary/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_apiary__get(async_app):
    data = {"name": "a name", "honey_kind": "too good", "location": "everywhere"}
    response = await async_app.post("/apiary", json=data)
    assert response.status_code == 201, response.text

    swarm_id = response.json()["public_id"]
    response = await async_app.get(f"/apiary/{swarm_id}")
    assert response.status_code == 200, response.text
    assert len(response.json()) >= 1


@pytest.mark.parametrize("async_app", ["22222222-2222-2222-2222-222222222222"], indirect=True)
async def test_list_apiaries(async_app, session):
    apiaries = ApiaryModelFactory.build_batch(5, organization_id="22222222-2222-2222-2222-222222222222")
    hives = [HiveModelFactory.create(apiary=apiary) for apiary in apiaries]
    session.add_all(apiaries)
    session.add_all(hives)
    await session.commit()

    response = await async_app.get("/apiary")

    assert response.status_code == 200, response.text
    assert len(response.json()) == 5, response.text
    data = response.json()
    for apiary in data:
        assert apiary["hive_count"] == 1


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
@pytest.mark.parametrize(
    "payload",
    (
        {"honey_kind": "new honey_kind"},
        {"location": "new location"},
        {"name": "new name"},
    ),
)
async def test_put_apiary__success(async_app, payload):
    data = {"name": "a name", "honey_kind": "too good", "location": "everywhere"}
    response = await async_app.post("/apiary", json=data)
    assert response.status_code == 201, response.text
    apiary_id = response.json()["public_id"]

    response = await async_app.put(f"/apiary/{apiary_id}", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in payload.items():
        assert data[key] == value


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_delete_apiary__success(async_app):
    data = {"name": "a name", "honey_kind": "too good", "location": "everywhere"}
    response = await async_app.post("/apiary", json=data)
    assert response.status_code == 201, response.text
    apiary_id = response.json()["public_id"]

    response = await async_app.delete(f"/apiary/{apiary_id}")
    assert response.status_code == 204, response.text

    response = await async_app.get(f"/apiary/{apiary_id}")
    assert response.status_code == 404, response.text
