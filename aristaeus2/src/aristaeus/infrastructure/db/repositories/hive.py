from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import joinedload

from aristaeus.domain.adapters.repositories.hive import HiveRepositoryAdapter
from aristaeus.domain.entities.hive import DetailedHiveEntity, HiveEntity
from aristaeus.infrastructure.db.engine import AsyncDatabase
from aristaeus.infrastructure.db.models.apiary import ApiaryModel
from aristaeus.infrastructure.db.models.hive import HiveModel
from aristaeus.infrastructure.db.models.swarm import SwarmModel
from aristaeus.infrastructure.db.utils import error_handler, get_data_from_entity
from aristaeus.injector import Injector


@Injector.bind(HiveRepositoryAdapter)
class HiveRepository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> HiveEntity:
        query = select(HiveModel).where(HiveModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.unique().scalar_one().to_entity()

    @error_handler
    async def save(self, hive: HiveEntity) -> None:
        data = get_data_from_entity(hive)

        if "apiary_id" in data:
            sub_query = select(ApiaryModel.id).where(ApiaryModel.public_id == data["apiary_id"])
            data["apiary_id"] = sub_query

        if "swarm_id" in data:
            sub_query = select(SwarmModel.id).where(SwarmModel.public_id == data["swarm_id"])
            data["swarm_id"] = sub_query

        query = insert(HiveModel).values(data)
        await self.database.execute(query)

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
    async def list(self, organization_id: UUID) -> list[DetailedHiveEntity]:
        query = (
            select(HiveModel)
            .options(joinedload(HiveModel.apiary), joinedload(HiveModel.swarm))
            .where(HiveModel.organization_id == organization_id)
        )

        result = await self.database.execute(query)
        return [model.to_detailed_entity() for model in result.unique().scalars()]
