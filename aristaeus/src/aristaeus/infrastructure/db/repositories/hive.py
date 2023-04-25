from typing import Any
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload

from aristaeus.domain.adapters.repositories.hive import HiveRepositoryAdapter
from aristaeus.domain.entities.hive import HiveEntity
from aristaeus.infrastructure.db.engine import AsyncDatabase
from aristaeus.infrastructure.db.models.apiary import ApiaryModel
from aristaeus.infrastructure.db.models.hive import HiveModel
from aristaeus.infrastructure.db.models.swarm import SwarmModel
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.injector import Injector


@Injector.bind(HiveRepositoryAdapter)
class HiveRepository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> HiveEntity:
        query = (
            select(HiveModel)
            .options(joinedload(HiveModel.apiary), joinedload(HiveModel.swarm))
            .where(HiveModel.public_id == public_id)
        )
        result = await self.database.execute(query)
        return result.unique().scalar_one().to_entity()

    def _get_relation_queries(self, hive: HiveEntity) -> dict:
        data = {}
        apiary_id = hive.apiary.public_id if hive.apiary else None
        swarm_id = hive.swarm.public_id if hive.swarm else None

        if apiary_id:
            sub_query = select(ApiaryModel.id).where(ApiaryModel.public_id == apiary_id).scalar_subquery()
            data["apiary_id"] = sub_query

        if swarm_id:
            sub_query = select(SwarmModel.id).where(SwarmModel.public_id == swarm_id).scalar_subquery()
            data["swarm_id"] = sub_query

        return data

    @error_handler
    async def save(self, hive: HiveEntity) -> None:
        data: dict[Any, Any] = {
            "name": hive.name,
            "condition": hive.condition,
            "owner": hive.owner,
            "public_id": hive.public_id,
            "organization_id": hive.organization_id,
        }
        data.update(self._get_relation_queries(hive))

        query = insert(HiveModel).values(data)
        await self.database.execute(query)

    @error_handler
    async def update(self, hive: HiveEntity) -> None:
        data: dict[Any, Any] = {
            "name": hive.name,
            "condition": hive.condition,
            "owner": hive.owner,
        }
        data.update(self._get_relation_queries(hive))
        query = update(HiveModel).values(data).where(HiveModel.public_id == hive.public_id)
        await self.database.execute(query)

    @error_handler
    async def delete(self, hive: HiveEntity) -> None:
        query = delete(HiveModel).where(HiveModel.public_id == hive.public_id)
        await self.database.execute(query)

    @error_handler
    async def list(self, organization_id: UUID) -> list[HiveEntity]:
        query = (
            select(HiveModel)
            .options(joinedload(HiveModel.apiary), joinedload(HiveModel.swarm))
            .where(HiveModel.organization_id == organization_id)
        )

        result = await self.database.execute(query)
        return [model.to_entity() for model in result.unique().scalars()]
