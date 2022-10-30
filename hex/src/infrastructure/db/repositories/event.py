import asyncio
import functools
from sqlalchemy import select

from domains.bee.entities.event import EventEntity
from domains.bee.errors import EntitySavingError
from infrastructure.db.models.event import EventModel
from infrastructure.db.repositories.base import BaseRepository
from domains.bee.entities.vo.reference import Reference
import functools


class EventRepository(BaseRepository):
    async def get_async(self, reference: Reference) -> EventEntity:
        query = select(EventModel).where(EventModel.public_id == reference.get())
        result = await self.database.execute_async(query)
        return result.scalar_one().to_entity()

    async def save_async(self, entity: EventEntity) -> None:
        model = EventModel.from_entity(entity)
        await self.database.save_async(model)
