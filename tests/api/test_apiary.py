import uuid
import pytest

from tests.factories import ApiaryModelFactory


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_apiary(async_app):
    data = {"name": "a name", "honey_kind": "too good", "location": "everywhere"}
    response = await async_app.post("/apiary", json=data)
    assert response.status_code == 200, response.text

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
    assert response.status_code == 200, response.text

    swarm_id = response.json()["public_id"]
    response = await async_app.get(f"/apiary/{swarm_id}")
    assert response.status_code == 200, response.text


@pytest.mark.parametrize("async_app", ["22222222-2222-2222-2222-222222222222"], indirect=True)
async def test_list_hives(async_app, session):
    apiaries = ApiaryModelFactory.build_batch(5, organization_id="22222222-2222-2222-2222-222222222222")
    session.add_all(apiaries)
    await session.commit()

    response = await async_app.get("/apiary")

    assert response.status_code == 200, response.text
    assert len(response.json()) == 5, response.text
