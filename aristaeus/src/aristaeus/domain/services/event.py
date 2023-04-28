from uuid import UUID

from aristaeus.domain.adapters.repositories.event import EventRepositoryAdapter
from aristaeus.domain.adapters.repositories.hive import HiveRepositoryAdapter
from aristaeus.domain.commands.event import CreateEventCommand
from aristaeus.domain.commands.event import PutEventCommand
from aristaeus.domain.entities.event import Event
from aristaeus.injector import InjectorMixin


class EventApplication(InjectorMixin):
    event_repository: EventRepositoryAdapter
    hive_repository: HiveRepositoryAdapter

    async def create(self, command: CreateEventCommand) -> Event:
        hive = await self.hive_repository.get(command.hive_id)
        event = Event(
            title=command.title,
            description=command.description,
            status=command.status,
            type=command.type,
            due_date=command.due_date,
            hive=hive,
        )
        await self.event_repository.save(event)
        return event

    async def put(self, command: PutEventCommand) -> Event:
        event = await self.event_repository.get(command.event_id)

        if title := command.title:
            event.change_title(title)
        if due_date := command.due_date:
            event.change_due_date(due_date)
        if description := command.description:
            event.change_description(description)
        if status := command.status:
            event.new_status(status)

        await self.event_repository.update(event=event)
        return event

    async def delete(self, event_id: UUID) -> None:
        event = await self.event_repository.get(event_id)
        await self.event_repository.delete(event)
