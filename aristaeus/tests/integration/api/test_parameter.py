import pytest


@pytest.mark.parametrize("async_app", ["66666666-6666-6666-6666-666666666666"], indirect=True)
async def test_parameter_endpoint(async_app):
    # CREATE
    data = {
        "key": "key",
        "value": "value",
    }
    response = await async_app.post("/parameter", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["key"] == "key", data

    parameter_id = data["public_id"]

    # GET
    response = await async_app.get(f"/parameter/{parameter_id}")
    assert response.status_code == 200, response.text
    assert data["value"] == "value", response.text

    # UPDATE
    response = await async_app.put(f"/parameter/{parameter_id}", json={"value": "new value"})
    assert response.status_code == 200, response.text
    assert response.json()["value"] == "new value", response.text

    # LIST
    response = await async_app.get("/parameter", params={"key": "key"})
    assert response.status_code == 200, response.text

    data = response.json()
    assert len(data) == 1
    assert data[0]["value"] == "new value", response.text

    # DELETE
    response = await async_app.delete(f"/parameter/{parameter_id}")
    assert response.status_code == 204, response.text
    response = await async_app.get(f"/parameter/{parameter_id}")
    assert response.status_code == 404, response.text
