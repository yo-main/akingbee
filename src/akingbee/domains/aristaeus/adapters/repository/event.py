from typing import Protocol
from typing import TYPE_CHECKING

from domains.bee.entities.event import EventEntity
from domains.bee.entities.vo.reference import Reference

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class EventRepositoryAdapter(Base):
    async def save_async(self, entity: EventEntity) -> None:
        ...

    async def get_async(self, reference: Reference) -> EventEntity:
        ...
