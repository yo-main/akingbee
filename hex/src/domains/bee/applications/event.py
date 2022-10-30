from domains.bee.adapters.repository.event import EventRepositoryAdapter
from domains.bee.adapters.repository.hive import HiveRepositoryAdapter
from domains.bee.commands.create_event import CreateEventCommand
from domains.bee.entities.event import EventEntity
from domains.bee.entities.vo.reference import Reference


class EventApplication:
    def __init__(
        self,
        event_repository: EventRepositoryAdapter,
        hive_repository: HiveRepositoryAdapter,
    ):
        self.hive_repository = hive_repository
        self.event_repository = event_repository

    async def create_async(self, command: CreateEventCommand) -> EventEntity:
        hive_reference = Reference.of(command.hive)
        hive = await self.hive_repository.get_async(hive_reference)

        event = EventEntity.create(
            title=command.title,
            description=command.description,
            status=command.status,
            type=command.type,
            due_date=command.due_date,
            hive=hive,
        )
        await self.event_repository.save_async(event)
        return event
