from dataclasses import dataclass, field
from typing import Awaitable, Generic, TypeVar

import anyio
from sqlalchemy.exc import NoResultFound

from aristaeus.domain.errors import EntityNotFound

_type = TypeVar("_type")


@dataclass
class Result(Generic[_type]):
    is_awaitable: bool
    value: Awaitable[_type] | _type
    dependant_tasks: list[Awaitable] = field(default_factory=list)

    @classmethod
    def of(cls, value, dependent_tasks: list = None) -> "Result":
        if not dependent_tasks:
            return Result(value=value, is_awaitable=isinstance(value, Awaitable))

        tasks = [task.value if isinstance(task, cls) else task for task in dependent_tasks]

        return Result(value=value, is_awaitable=isinstance(value, Awaitable), dependant_tasks=tasks)

    async def retrieve_result(self):
        for task in self.dependant_tasks:
            await task

        if not self.is_awaitable:
            return self.value

        try:
            return await self.value
        except NoResultFound as exc:
            raise EntityNotFound("Not Found") from exc
