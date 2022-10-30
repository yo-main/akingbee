from typing import Protocol
from sqlalchemy.sql.expression import Executable
from sqlalchemy.engine import Result

from infrastructure.db.models.base import BaseModel


class BaseDatabase(Protocol):
    async def save_async(self, entity: BaseModel) -> None:
        ...

    async def execute_async(self, query: Executable) -> Result:
        ...


class BaseRepository:
    def __init__(self, database: BaseDatabase):
        self.database = database
