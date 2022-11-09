import asyncio
import functools
from sqlalchemy import select

from domains.bee.entities.swarm import SwarmEntity
from domains.bee.errors import EntitySavingError
from domains.bee.adapters.repository.swarm import SwarmRepositoryAdapter
from infrastructure.db.models.swarm import SwarmModel
from infrastructure.db.engine import AsyncDatabase
from domains.bee.entities.vo.reference import Reference
from injector import Injector


@Injector.bind(SwarmRepositoryAdapter)
class SwarmRespository:
    database: AsyncDatabase

    async def get_async(self, reference: Reference) -> SwarmEntity:
        query = select(SwarmModel).where(SwarmModel.public_id == reference.get())
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    async def save_async(self, entity: SwarmEntity) -> None:
        model = SwarmModel.from_entity(entity)
        await self.database.save(model)
