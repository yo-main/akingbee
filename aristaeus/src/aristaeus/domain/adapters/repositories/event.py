from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.event import EventEntity

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class EventRepositoryAdapter(Base):
    async def save(self, event: EventEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> EventEntity:
        ...

    async def update(self, event: EventEntity, fields: list[str]) -> EventEntity:
        ...

    async def delete(self, event: EventEntity) -> None:
        ...

    async def list(self, hive_id: UUID) -> list[EventEntity]:
        ...
