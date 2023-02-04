from uuid import UUID

from aristaeus.domain.adapters.repositories.event import EventRepositoryAdapter
from aristaeus.domain.commands.event import CreateEventCommand
from aristaeus.domain.commands.event import PutEventCommand
from aristaeus.domain.entities.event import EventEntity
from aristaeus.injector import InjectorMixin


class EventApplication(InjectorMixin):
    event_repository: EventRepositoryAdapter

    async def create(self, command: CreateEventCommand) -> EventEntity:
        event = EventEntity(
            title=command.title,
            description=command.description,
            status=command.status,
            type=command.type,
            due_date=command.due_date,
            hive_id=command.hive_id,
        )
        await self.event_repository.save(event)
        return event

    async def put(self, command: PutEventCommand) -> EventEntity:
        event = await self.event_repository.get(command.event_id)
        new_event, updated_fields = event.update(
            due_date=command.due_date,
            status=command.status,
            title=command.title,
            description=command.description,
        )

        await self.event_repository.update(event=new_event, fields=updated_fields)
        return new_event

    async def delete(self, event_id: UUID) -> None:
        event = await self.event_repository.get(event_id)
        await self.event_repository.delete(event)