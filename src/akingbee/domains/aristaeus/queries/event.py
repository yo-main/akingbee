from uuid import UUID
from akingbee.domains.aristaeus.entities.event import EventEntity
from akingbee.infrastructure.db.repositories.event import EventRepositoryAdapter

from akingbee.injector import InjectorMixin


class EventQuery(InjectorMixin):
    event_repository: EventRepositoryAdapter

    async def get_event_query(self, event_id: UUID) -> EventEntity:
        return await self.event_repository.get(event_id)
