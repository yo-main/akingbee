import uuid

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from aristaeus.config import settings
from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.domain.entities.user import User
from aristaeus.dispatcher import Dispatcher

settings.setenv("test")

from aristaeus.controllers.api.app import create_app

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def app():
    with TestClient(app=create_app(), base_url="http://testserver") as client:
        client.cookies["access_token"] = "test"
        yield client


@pytest.fixture(scope="session", autouse=True)
async def async_app(anyio_backend, request):
    async with AsyncClient(app=create_app(), base_url="http://testserver") as client:
        if hasattr(request, "param"):
            access_token = uuid.UUID(request.param)
            async with UnitOfWork() as uow:
                user = User(public_id=access_token, organization_id=access_token)
                await uow.user.save(user)

            client.cookies["access_token"] = str(access_token)
        yield client
