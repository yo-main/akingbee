from typing import Protocol

from infrastructure.db.models.base import BaseModel
from infrastructure.db.repositories.base import BaseDatabaseAsync
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.sql.expression import Executable
from sqlalchemy import Result


class DatabaseAsync(BaseDatabaseAsync):
    def __init__(self):
        self._engine = create_async_engine("postgresql+asycncpg://admin:password@localhost:5432/akingbee_v2")
        self._session_maker = async_sessionmaker(self.engine)

    async def save(self, entity: BaseModel) -> None:
        async with self._session_maker() as session:
            await session.save(entity)

    async def execute(self, query: Executable) -> Result:
        async with self._session_maker() as session:
            return await session.execute(query)
