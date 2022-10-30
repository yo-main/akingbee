import asyncio
import functools
from sqlalchemy import select

from domains.bee.entities.swarm import SwarmEntity
from domains.bee.errors import EntitySavingError
from infrastructure.db.models.swarm import SwarmModel
from infrastructure.db.repositories.base import BaseRepository
from domains.bee.entities.vo.reference import Reference


class SwarmRepository(BaseRepository):
    async def get_async(self, reference: Reference) -> SwarmEntity:
        query = select(SwarmModel).where(SwarmModel.public_id == reference.get())
        result = await self.database.execute_async(query)
        return result.scalar_one().to_entity()

    async def save_async(self, entity: SwarmEntity) -> None:
        model = SwarmModel.from_entity(entity)
        await self.database.save_async(model)
