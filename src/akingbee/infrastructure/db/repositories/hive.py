from uuid import UUID

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete

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
    async def save(self, hive: HiveEntity) -> None:
        model = HiveModel.from_entity(hive)
        await self.database.save(model)

    @error_handler
    async def update(self, hive: HiveEntity, fields: list[str]) -> HiveEntity:
        query = (
            update(HiveModel)
            .values({field: getattr(hive, field) for field in fields})
            .where(HiveModel.public_id == hive.public_id)
        )
        await self.database.execute(query)
        return await self.get(hive.public_id)

    @error_handler
    async def delete(self, hive: HiveEntity) -> None:
        query = delete(HiveModel).where(HiveModel.public_id == hive.public_id)
        await self.database.execute(query)

    @error_handler
    async def list(self, organization_id: UUID) -> list[HiveEntity]:
        query = select(HiveModel).where(HiveModel.organization_id == organization_id)
        result = await self.database.execute(query)
        return [model.to_entity() for model in result.scalars()]
