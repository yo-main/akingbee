from uuid import UUID

from aristaeus.domain.entities.event import Event
from aristaeus.infrastructure.db.repositories.event import EventRepositoryAdapter
from aristaeus.injector import InjectorMixin


class EventQuery(InjectorMixin):
    event_repository: EventRepositoryAdapter

    async def get_event_query(self, event_id: UUID) -> Event:
        return await self.event_repository.get(event_id)

    async def list_event_query(self, event_id: UUID) -> list[Event]:
        return await self.event_repository.list(event_id)
