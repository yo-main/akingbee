from akingbee.domains.aristaeus.adapters.repositories.event import EventRepositoryAdapter
from akingbee.domains.aristaeus.commands.create_event import CreateEventCommand
from akingbee.domains.aristaeus.entities.event import EventEntity
from akingbee.domains.aristaeus.entities.vo.reference import Reference
from akingbee.injector import InjectorMixin


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
