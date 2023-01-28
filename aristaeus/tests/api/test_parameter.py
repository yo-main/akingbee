import uuid

import pytest
from tests.factories import ParameterModelFactory


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_parameter(async_app):
    data = {
        "key": "key",
        "value": "value",
    }
    response = await async_app.post("/parameter", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["key"] == "key", data
    assert data["value"] == "value", data
    assert data["organization_id"] == "11111111-1111-1111-1111-111111111111", data


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
@pytest.mark.parametrize(
    "payload",
    (
        {"key": None},
        {"value": None},
    ),
)
async def test_create_parameter__wrong_payload(async_app, payload):
    data = {"key": "key", "value": "value"}
    data.update(payload)
    data = {k: v for k, v in data.items() if v is not None}
    response = await async_app.post("/parameter", json=data)
    assert response.status_code == 422, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_parameter__unknown(async_app):
    response = await async_app.get(f"/parameter/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_parameter(async_app):
    data = {
        "key": "key2",
        "value": "value2",
    }
    response = await async_app.post("/parameter", json=data)
    assert response.status_code == 200, response.text

    parameter_id = response.json()["public_id"]
    response = await async_app.get(f"/parameter/{parameter_id}")
    assert response.status_code == 200, response.text


@pytest.mark.parametrize("async_app", ["22222222-2222-2222-2222-222222222222"], indirect=True)
async def test_list_parameters__without_key(async_app, session):
    parameters = ParameterModelFactory.build_batch(5, key="abc", organization_id="22222222-2222-2222-2222-222222222222")
    session.add_all(parameters)
    await session.commit()

    response = await async_app.get("/parameter")

    assert response.status_code == 200, response.text
    assert len(response.json()) == 5, response.text


@pytest.mark.parametrize("async_app", ["22222222-2222-2222-2222-222222222222"], indirect=True)
async def test_list_parameters__with_key(async_app, session):
    parameters = ParameterModelFactory.build_batch(3, key="def", organization_id="22222222-2222-2222-2222-222222222222")
    session.add_all(parameters)
    await session.commit()

    response = await async_app.get("/parameter", params={"key": "def"})

    assert response.status_code == 200, response.text
    assert len(response.json()) == 3, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_put_parameter__success(async_app, session):
    parameter = ParameterModelFactory.build(organization_id="11111111-1111-1111-1111-111111111111", value="old")
    session.add(parameter)
    await session.commit()
    await session.refresh(parameter)

    response = await async_app.put(f"/parameter/{parameter.public_id}", json={"value": "new"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["public_id"] == str(parameter.public_id)
    assert data["value"] == "new"


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_delete_parameter__success(async_app, session):
    parameter = ParameterModelFactory.build(organization_id="11111111-1111-1111-1111-111111111111", value="old")
    session.add(parameter)
    await session.commit()
    await session.refresh(parameter)

    response = await async_app.delete(f"/parameter/{parameter.public_id}")
    assert response.status_code == 204, response.text

    response = await async_app.get(f"/parameter/{parameter.public_id}")
    assert response.status_code == 404, response.text
