from typing import Any
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from aristaeus.domain.adapters.repositories.event import EventRepositoryAdapter
from aristaeus.domain.entities.event import Event
from aristaeus.domain.errors import EntityNotFound
from aristaeus.infrastructure.db import orm
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.injector import Injector

from .base import BaseRepository


@Injector.bind(EventRepositoryAdapter, "test")
class FakeEventRepository(BaseRepository):
    _events: set[Event] = set()

    async def get(self, public_id: UUID) -> Event:
        try:
            return next(event for event in self._events if event.public_id == public_id)
        except StopIteration:
            raise EntityNotFound("Event not found")

    async def save(self, event: Event) -> None:
        self._events.add(event)

    async def update(self, event: Event) -> None:
        self._events.discard(event)
        self._events.add(event)

    async def list(self, hive_id: UUID) -> list[Event]:
        return [event for event in self._events if event.hive.public_id == hive_id]

    async def delete(self, event: Event) -> None:
        self._events.discard(event)


@Injector.bind(EventRepositoryAdapter)
class EventRepository(BaseRepository):
    @error_handler
    async def get(self, public_id: UUID) -> Event:
        query = select(Event).where(orm.event_table.c.public_id == public_id)
        result = await self.session.execute(query)
        return result.unique().scalar_one()

    @error_handler
    async def save(self, event: Event) -> None:
        data = {
            "title": event.title,
            "description": event.description,
            "due_date": event.due_date,
            "type": event.type,
            "status": event.status,
            "public_id": event.public_id,
            "hive_id": select(orm.hive_table.c.id).where(orm.hive_table.c.public_id == event.hive.public_id),
        }

        query = insert(orm.event_table).values(data)
        await self.session.execute(query)

    @error_handler
    async def update(self, event: Event) -> None:
        data: dict[Any, Any] = {
            "title": event.title,
            "description": event.description,
            "status": event.status,
            "due_date": event.due_date,
        }
        query = update(orm.event_table).values(data).where(orm.event_table.c.public_id == event.public_id)
        await self.session.execute(query)

    @error_handler
    async def delete(self, event: Event) -> None:
        query = delete(orm.event_table).where(orm.event_table.c.public_id == event.public_id)
        await self.session.execute(query)

    @error_handler
    async def list(self, hive_id: UUID) -> list[Event]:
        query = select(Event).join_from(orm.hive_table, orm.event_table).where(orm.hive_table.c.public_id == hive_id)
        result = await self.session.execute(query)
        return result.unique().scalars().all()
