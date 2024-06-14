from uuid import UUID

from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.domain.commands.event import CreateEventCommand
from aristaeus.domain.commands.event import PutEventCommand
from aristaeus.domain.entities.event import Event
from aristaeus.injector import InjectorMixin


class EventApplication(InjectorMixin):
    async def create(self, command: CreateEventCommand) -> Event:
        async with UnitOfWork() as uow:
            hive = await uow.hive.get(command.hive_id)
            event = Event(
                title=command.title,
                description=command.description,
                status=command.status,
                type=command.type,
                due_date=command.due_date,
                hive=hive,
            )
            await uow.event.save(event)
            await uow.commit()

        return event

    async def put(self, command: PutEventCommand) -> Event:
        async with UnitOfWork() as uow:
            event = await uow.event.get(command.event_id)

            if title := command.title:
                event.change_title(title)
            if due_date := command.due_date:
                event.change_due_date(due_date)
            if description := command.description:
                event.change_description(description)
            if status := command.status:
                event.new_status(status)

            await uow.event.update(event=event)
            await uow.commit()

        return event

    async def delete(self, event_id: UUID) -> None:
        async with UnitOfWork() as uow:
            event = await uow.event.get(event_id)
            await uow.event.delete(event)
            await uow.commit()
