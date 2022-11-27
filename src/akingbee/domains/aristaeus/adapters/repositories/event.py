from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from akingbee.domains.aristaeus.entities.event import EventEntity

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class EventRepositoryAdapter(Base):
    async def save(self, event: EventEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> EventEntity:
        ...
