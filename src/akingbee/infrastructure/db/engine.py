from typing import Protocol

from infrastructure.db.models.base import BaseModel
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.sql.expression import Executable
from sqlalchemy import Result

from utils.singleton import SingletonMeta
from injector import Injector


from infrastructure.db.models.base import BaseModel


class AsyncDatabase(Protocol):
    async def save(self, entity: BaseModel) -> None:
        ...

    async def execute(self, query: Executable) -> Result:
        ...


@Injector.bind(AsyncDatabase, "development", "test")
class PostgresAsync(metaclass=SingletonMeta):
    def __init__(self):
        self._engine = create_async_engine("postgresql+asyncpg://admin:password@localhost:5432/akingbee_v2")
        self._session_maker = async_sessionmaker(self._engine)

    async def save(self, entity: BaseModel) -> None:
        async with self._session_maker() as session:
            await session.save(entity)

    async def execute(self, query: Executable) -> Result:
        async with self._session_maker() as session:
            return await session.execute(query)
