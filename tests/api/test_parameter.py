import uuid
import pytest


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
    hive_id = str(uuid.uuid4())
    data = {
        "key": "key",
        "value": "value",
    }
    response = await async_app.post("/parameter", json=data)
    assert response.status_code == 200, response.text

    parameter_id = response.json()["public_id"]
    response = await async_app.get(f"/parameter/{parameter_id}")
    assert response.status_code == 200, response.text

