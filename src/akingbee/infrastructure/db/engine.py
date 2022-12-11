from contextlib import asynccontextmanager
from typing import AsyncIterator, Protocol

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.sql.expression import Executable

from akingbee.infrastructure.db.models.base import BaseModel
from akingbee.infrastructure.db.utils import get_database_uri
from akingbee.injector import Injector
from akingbee.utils.singleton import SingletonMeta


class AsyncDatabase(Protocol):
    async def save(self, entity: BaseModel, commit: bool) -> None:
        ...

    async def execute(self, query: Executable) -> Result:
        ...

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        ...


@Injector.bind(AsyncDatabase, "development", "test")
class PostgresAsync(metaclass=SingletonMeta):
    def __init__(self):
        self.init()

    def init(self):
        self._engine = create_async_engine(get_database_uri())
        self._session_maker = async_sessionmaker(self._engine)

    async def save(self, entity: BaseModel, commit: bool) -> None:
        async with self._session_maker() as session:
            session.add(entity)
            if commit:
                await session.commit()

    async def execute(self, query: Executable) -> Result:
        async with self._session_maker() as session:
            return await session.execute(query)

    async def close(self):
        await self._engine.dispose(close=True)

    async def reset(self):
        await self.close()
        await self.init()

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self._session_maker() as session:
            yield session


@Injector.bind(AsyncDatabase, "test-simple")
class PostgresAsyncTest(metaclass=SingletonMeta):
    def __init__(self):
        self.init()

    def init(self):
        self._engine = create_async_engine(get_database_uri())
        self._session_maker = async_sessionmaker(self._engine)
        self.session = self._session_maker()

    async def save(self, entity: BaseModel, commit: bool) -> None:
        self.session.add(entity)
        if commit:
            await self.session.commit()

    async def execute(self, query: Executable) -> Result:
        return await self.session.execute(query)

    async def close(self):
        await self.session.rollback()

    async def reset(self):
        await self.close()
        self.init()

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        yield self.session
