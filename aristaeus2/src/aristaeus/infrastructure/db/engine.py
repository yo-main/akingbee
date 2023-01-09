from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Protocol

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.sql.expression import Executable

from aristaeus.infrastructure.db.models.base import BaseModel
from aristaeus.infrastructure.db.utils import get_database_uri
from aristaeus.injector import Injector
from aristaeus.utils.singleton import SingletonMeta


class AsyncDatabase(Protocol):
    async def execute(self, query: Executable) -> Result:
        ...

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        ...

    async def reset(self) -> None:
        ...


@Injector.bind(AsyncDatabase, "development", "test")
class PostgresAsync(metaclass=SingletonMeta):
    def __init__(self):
        self.init()

    def init(self):
        self._engine = create_async_engine(get_database_uri())
        self._session_maker = async_sessionmaker(self._engine)

    async def execute(self, query: Executable) -> Result:
        async with self._session_maker() as session:
            result = await session.execute(query)
            if query.is_insert or query.is_update or query.is_delete:
                await session.commit()
            return result

    async def close(self):
        await self._engine.dispose(close=True)

    async def reset(self):
        await self.close()
        await self.init()

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self._session_maker() as session:
            yield session
