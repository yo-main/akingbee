import asyncio
import functools
from uuid import UUID

from sqlalchemy import select

from akingbee.domains.aristaeus.adapters.repositories.event import (
    EventRepositoryAdapter,
)
from akingbee.domains.aristaeus.entities.event import EventEntity
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.models.event import EventModel
from akingbee.infrastructure.db.utils import error_handler
from akingbee.injector import Injector


@Injector.bind(EventRepositoryAdapter)
class EventRepository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> EventEntity:
        query = select(EventModel).where(EventModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    @error_handler
    async def save(self, entity: EventEntity) -> None:
        model = EventModel.from_entity(entity)
        await self.database.save(model)
