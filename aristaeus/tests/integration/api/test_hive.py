import pytest


@pytest.mark.parametrize("async_app", ["22222222-2222-2222-2222-222222222222"], indirect=True)
async def test_hive_endpoints(async_app):

    # create apiary
    data = {"name": "apiary name", "honey_kind": "honey kind", "location": "location"}
    response = await async_app.post("/apiary", json=data)
    assert response.status_code == 201, response.text

    apiary_id = response.json()["public_id"]

    # create hive
    data = {"name": "hive name", "condition": "condition", "owner": "owner", "apiary_id": apiary_id}
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 201, response.text

    data = response.json()
    assert data["name"] == "hive name", data

    hive_id = data["public_id"]

    # get hive
    response = await async_app.get(f"hive/{hive_id}")
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "hive name", response.text

    # update hive
    response = await async_app.put(f"hive/{hive_id}", json={"name": "new name"})
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "new name", response.text

    # list hive
    response = await async_app.get("hive")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "new name", response.text


@pytest.mark.parametrize("async_app", ["22222222-2222-2222-2222-222222222222"], indirect=True)
async def test_hive_move(async_app):

    # create apiary
    data = {"name": "second apiary name", "honey_kind": "honey kind", "location": "location"}
    response = await async_app.post("/apiary", json=data)
    assert response.status_code == 201, response.text

    apiary_id = response.json()["public_id"]

    # create hive
    data = {"name": "second hive name", "condition": "condition", "owner": "owner"}
    response = await async_app.post("/hive", json=data)
    assert response.status_code == 201, response.text

    data = response.json()
    assert data["apiary"] is None, data

    hive_id = data["public_id"]

    # move hive
    response = await async_app.put(f"hive/{hive_id}/move/{apiary_id}")
    assert response.status_code == 200, response.text
    assert response.json()["apiary"]["public_id"] == apiary_id, response.text

