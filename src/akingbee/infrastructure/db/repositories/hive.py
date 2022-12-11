from uuid import UUID

from sqlalchemy import select

from akingbee.domains.aristaeus.adapters.repositories.hive import HiveRepositoryAdapter
from akingbee.domains.aristaeus.entities.hive import HiveEntity
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.models.hive import HiveModel
from akingbee.infrastructure.db.utils import error_handler
from akingbee.injector import Injector


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
        await self.database.save(model)

    @error_handler
    async def list(self, organization_id: UUID) -> list[HiveEntity]:
        query = select(HiveModel).where(HiveModel.organization_id == organization_id)
        result = await self.database.execute(query)
        return [model.to_entity() for model in result.scalars()]
