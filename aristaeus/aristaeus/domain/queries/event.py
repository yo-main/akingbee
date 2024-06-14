from uuid import UUID

from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.domain.entities.event import Event
from aristaeus.injector import InjectorMixin


class EventQuery(InjectorMixin):
    async def get_event_query(self, event_id: UUID) -> Event:
        async with UnitOfWork() as uow:
            return await uow.event.get(event_id)

    async def list_event_query(self, event_id: UUID) -> list[Event]:
        async with UnitOfWork() as uow:
            return await uow.event.list(event_id)
