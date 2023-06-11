import uuid
from datetime import datetime

import jwt
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from aristaeus.config import settings

settings.setenv("integration")

from aristaeus.controllers.api.app import create_app
from aristaeus.infrastructure.db.orm.base import mapper_registry
from aristaeus.infrastructure.db.utils import get_database_uri

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def root_engine():
    engine = create_async_engine(get_database_uri("postgres"))
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def root_connection(root_engine):
    connection = await root_engine.connect()
    yield connection
    await connection.close()


@pytest.fixture(scope="session")
def dbname():
    dbname = "test_" + str(uuid.uuid4()).replace("-", "")
    settings.set("database_dbname", dbname)
    return dbname


@pytest.fixture(scope="session")
async def provision_database(dbname, root_connection):
    await root_connection.execute(text("commit"))
    await root_connection.execute(text(f"CREATE DATABASE {dbname}"))
    await root_connection.execute(text("commit"))

    url = get_database_uri(dbname)
    engine = create_async_engine(url)

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
        await conn.commit()

    yield engine

    await engine.dispose()

    await root_connection.execute(text("commit"))
    await root_connection.execute(
        text(
            f"""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{dbname}'
        AND pid <> pg_backend_pid();
    """
        )
    )
    await root_connection.execute(text(f"DROP DATABASE {dbname}"))
    await root_connection.close()


@pytest.fixture(scope="session", autouse=True)
async def app(provision_database):
    with TestClient(app=create_app(), base_url="http://testserver") as client:
        client.cookies["access_token"] = "test"
        yield client


@pytest.fixture(scope="session", autouse=True)
async def async_app(provision_database, anyio_backend, request):
    async with AsyncClient(app=create_app(), base_url="http://testserver") as client:
        if hasattr(request, "param"):
            access_token = request.param

            async with provision_database.begin() as conn:
                params = {"test_id": access_token, "date": datetime.now()}
                await conn.execute(
                    text(
                        """
                            INSERT INTO "user"(public_id, organization_id, date_creation, date_modification) 
                            VALUES (:test_id, :test_id, :date, :date)
                            ON CONFLICT DO NOTHING
                        """
                    ),
                    params,
                )
                await conn.commit()

            token = jwt.encode({"sub": str(access_token)}, key=settings.jwt_key, algorithm="HS256")
            client.cookies["access_token"] = str(token)
        yield client
