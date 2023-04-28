import pytest


@pytest.mark.parametrize("async_app", ["33333333-3333-3333-3333-333333333333"], indirect=True)
async def test_swarm_endpoints(async_app):
    # POST
    data = {"queen_year": 2020, "health": "Good"}
    response = await async_app.post("/swarm", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["queen_year"] == 2020, data

    swarm_id = data["public_id"]

    # GET
    response = await async_app.get(f"/swarm/{swarm_id}")
    assert response.status_code == 200, response.text
    assert response.json()["queen_year"] == 2020, response.text

    # UPDATE
    response = await async_app.put(f"/swarm/{swarm_id}", json={"queen_year": 2021})
    assert response.status_code == 200, response.text
    assert response.json()["queen_year"] == 2021, response.text

    # DELETE
    response = await async_app.delete(f"/swarm/{swarm_id}")
    assert response.status_code == 200, response.text

    response = await async_app.get(f"/swarm/{swarm_id}")
    assert response.status_code == 404, response.text
