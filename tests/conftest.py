import anyio
import pytest
import uuid
import contextlib
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy import Connection
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncConnection

from akingbee.config import settings

settings.setenv("test")

from akingbee.injector import Injector


from akingbee.controllers.api.aristaeus.app import create_app
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.utils import get_database_uri
from akingbee.infrastructure.db.models.base import BaseModel


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(get_database_uri("postgres"))
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def root_connection(engine):
    connection = await engine.connect()
    yield connection
    await connection.close()


@pytest.fixture(scope="session")
def dbname():
    dbname = "test_" + str(uuid.uuid4()).replace("-", "")
    settings.set("database_dbname", dbname)
    return dbname


@pytest.fixture(scope="session")
async def provision_database(dbname, root_connection, anyio_backend):
    await root_connection.execute(text("commit"))
    await root_connection.execute(text(f"CREATE DATABASE {dbname}"))
    await root_connection.execute(text("commit"))

    url = get_database_uri(dbname)
    engine = create_async_engine(url)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        await conn.commit()
    async with engine.begin() as conn:
        params = {"test_id": "11111111-1111-1111-1111-111111111111", "date": datetime.now()}
        await conn.execute(
            text(
                """INSERT INTO "user"(public_id, organization_id, date_creation, date_modification) VALUES (:test_id, :test_id, :date, :date)"""
            ),
            params,
        )
        await conn.commit()

    yield

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


@pytest.fixture(autouse=True)
async def session(anyio_backend):
    database = Injector.get(AsyncDatabase)
    async with database.get_session() as session:
        savepoint = await session.begin_nested()
        yield
        await savepoint.rollback()


@pytest.fixture(scope="session", autouse=True)
def app(provision_database):
    with TestClient(app=create_app()) as client:
        client.cookies["access_token"] = "test"
        yield client
