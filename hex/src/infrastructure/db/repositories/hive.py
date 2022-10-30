import asyncio
import functools
from sqlalchemy import select

from domains.bee.entities.hive import HiveEntity
from domains.bee.errors import EntitySavingError
from infrastructure.db.models.hive import HiveModel
from infrastructure.db.repositories.base import BaseRepository
from domains.bee.entities.vo.reference import Reference
import functools


class HiveRepository(BaseRepository):
    async def get_async(self, reference: Reference) -> HiveEntity:
        query = select(HiveModel).where(HiveModel.public_id == reference.get())
        result = await self.database.execute_async(query)
        return result.scalar_one().to_entity()

    async def save_async(self, entity: HiveEntity) -> None:
        model = HiveModel.from_entity(entity)
        await self.database.save_async(model)
