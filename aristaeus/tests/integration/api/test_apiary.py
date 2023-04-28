import pytest


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_apiary_endpoints(async_app):

    # POST
    data = {"name": "a name", "honey_kind": "too good", "location": "everywhere"}
    response = await async_app.post("/apiary", json=data)
    assert response.status_code == 201, response.text

    data = response.json()
    apiary_id = data["public_id"]

    # GET
    response = await async_app.get(f"/apiary/{apiary_id}")
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == "a name"

    # UPDATE
    response = await async_app.put(f"/apiary/{apiary_id}", json={"name": "new name"})
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == "new name"

    # LIST
    response = await async_app.get("/apiary")
    assert response.status_code == 200, response.text

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "new name"

    # DELETE
    response = await async_app.delete(f"/apiary/{apiary_id}")
    assert response.status_code == 204, response.text

    response = await async_app.get(f"/apiary/{apiary_id}")
    assert response.status_code == 404, response.text
