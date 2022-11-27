import asyncio
import functools
from uuid import UUID

from akingbee.domains.aristaeus.adapters.repositories.hive import HiveRepositoryAdapter
from akingbee.domains.aristaeus.entities.hive import HiveEntity
from akingbee.domains.aristaeus.entities.vo.reference import Reference
from akingbee.domains.aristaeus.errors import EntitySavingError
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.models.hive import HiveModel
from akingbee.infrastructure.db.utils import error_handler
from akingbee.injector import Injector
from sqlalchemy import select


@Injector.bind(HiveRepositoryAdapter)
class HiveRepository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> HiveEntity:
        query = select(HiveModel).where(HiveModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    @error_handler
    async def save(self, entity: HiveEntity) -> None:
        model = HiveModel.from_entity(entity)
        await self.database.save(model, commit=True)
