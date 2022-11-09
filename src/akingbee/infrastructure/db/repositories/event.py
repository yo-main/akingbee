import asyncio
import functools
from sqlalchemy import select

from domains.bee.entities.event import EventEntity
from domains.bee.errors import EntitySavingError
from domains.bee.adapters.repository.event import EventRepositoryAdapter
from infrastructure.db.models.event import EventModel
from infrastructure.db.engine import AsyncDatabase
from domains.bee.entities.vo.reference import Reference
from injector import Injector


@Injector.bind(EventRepositoryAdapter)
class EventRepository:
    database: AsyncDatabase

    async def get_async(self, reference: Reference) -> EventEntity:
        query = select(EventModel).where(EventModel.public_id == reference.get())
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    async def save_async(self, entity: EventEntity) -> None:
        model = EventModel.from_entity(entity)
        await self.database.save(model)
