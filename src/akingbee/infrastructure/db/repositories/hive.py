import asyncio
import functools
from sqlalchemy import select

from domains.bee.entities.hive import HiveEntity
from domains.bee.errors import EntitySavingError
from domains.bee.adapters.repository.hive import HiveRepositoryAdapter
from infrastructure.db.models.hive import HiveModel
from infrastructure.db.engine import AsyncDatabase
from domains.bee.entities.vo.reference import Reference
from injector import Injector


@Injector.bind(HiveRepositoryAdapter)
class HiveRepository:
    database: AsyncDatabase

    async def get_async(self, reference: Reference) -> HiveEntity:
        query = select(HiveModel).where(HiveModel.public_id == reference.get())
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    async def save_async(self, entity: HiveEntity) -> None:
        model = HiveModel.from_entity(entity)
        await self.database.save(model)
