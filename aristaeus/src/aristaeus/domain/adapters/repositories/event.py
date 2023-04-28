from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.event import Event

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class EventRepositoryAdapter(Base):
    async def save(self, event: Event) -> None:
        ...

    async def get(self, public_id: UUID) -> Event:
        ...

    async def update(self, event: Event) -> None:
        ...

    async def delete(self, event: Event) -> None:
        ...

    async def list(self, hive_id: UUID) -> list[Event]:
        ...
