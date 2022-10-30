from typing import Protocol

from domains.bee.entities.event import EventEntity
from domains.bee.entities.vo.reference import Reference


class EventRepositoryAdapter(Protocol):
    async def save_async(self, entity: EventEntity) -> None:
        ...

    async def get_async(self, reference: Reference) -> EventEntity:
        ...
