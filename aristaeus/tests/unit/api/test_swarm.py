import uuid

import pytest
from aristaeus.domain.adapters.repositories.swarm import SwarmRepositoryAdapter
from aristaeus.injector import Injector
from tests.factories import SwarmEntityFactory


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_swarm(async_app):
    data = {"queen_year": 2020, "health": "Good"}
    response = await async_app.post("/swarm", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["queen_year"] == 2020, data
    assert data["health"] == "Good", data


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
@pytest.mark.parametrize(
    "payload",
    (
        {"health": "Good"},
        {"queen_year": "Good"},
        {"health": "Ok", "queen_year": None},
        {"health": "Ok", "queen_year": ""},
        {"health": "", "queen_year": "bla"},
    ),
)
async def test_create_swarm__wrong_payload(async_app, payload):
    response = await async_app.post("/swarm", json=payload)
    assert response.status_code == 422, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_swarm__unknown(async_app):
    response = await async_app.get(f"/swarm/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_swarm__get(async_app):
    data = {"queen_year": 2010, "health": "Ok"}
    response = await async_app.post("/swarm", json=data)
    assert response.status_code == 200, response.text

    swarm_id = response.json()["public_id"]
    response = await async_app.get(f"/swarm/{swarm_id}")
    assert response.status_code == 200, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_put_swarm(async_app):
    swarm = SwarmEntityFactory()
    await Injector.get(SwarmRepositoryAdapter).save(swarm)

    data = {"health": "COUCOU"}

    response = await async_app.put(f"/swarm/{swarm.public_id}", json=data)
    assert response.status_code == 200, response.text
    assert response.json()["health"] == "COUCOU"


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_delete_swarm(async_app):
    swarm = SwarmEntityFactory()
    await Injector.get(SwarmRepositoryAdapter).save(swarm)

    response = await async_app.get(f"/swarm/{swarm.public_id}")
    assert response.status_code == 200, response.text

    response = await async_app.delete(f"/swarm/{swarm.public_id}")
    assert response.status_code == 200, response.text

    response = await async_app.get(f"/swarm/{swarm.public_id}")
    assert response.status_code == 404, response.text
