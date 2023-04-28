from typing import Any
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from aristaeus.domain.adapters.repositories.apiary import ApiaryRepositoryAdapter
from aristaeus.domain.entities.apiary import ApiaryEntity
from aristaeus.domain.errors import EntityNotFound
from aristaeus.infrastructure.db.engine import AsyncDatabase
from aristaeus.infrastructure.db import orm
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.injector import Injector


@Injector.bind(ApiaryRepositoryAdapter, "test")
class FakeApiaryRepository:
    _apiaries: set[ApiaryEntity] = set()

    async def get(self, public_id: UUID) -> ApiaryEntity:
        try:
            return next(apiary for apiary in self._apiaries if apiary.public_id == public_id)
        except StopIteration:
            raise EntityNotFound("Apiary not found")

    async def save(self, apiary: ApiaryEntity) -> None:
        self._apiaries.add(apiary)

    async def update(self, apiary: ApiaryEntity) -> None:
        self._apiaries.discard(apiary)
        self._apiaries.add(apiary)

    async def list(self, organization_id: UUID) -> list[ApiaryEntity]:
        return [apiary for apiary in self._apiaries if apiary.organization_id == organization_id]

    async def delete(self, apiary: ApiaryEntity) -> None:
        self._apiaries.discard(apiary)


@Injector.bind(ApiaryRepositoryAdapter)
class ApiaryRespository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> ApiaryEntity:
        query = (
            select(ApiaryEntity)
            .join_from(orm.apiary_table, orm.hive_table, isouter=True)
            .where(orm.apiary_table.c.public_id == public_id)
        )
        result = await self.database.execute(query)
        return result.unique().scalar_one()

    @error_handler
    async def save(self, apiary: ApiaryEntity) -> None:
        query = insert(orm.apiary_table).values(
            public_id=apiary.public_id,
            name=apiary.name,
            location=apiary.location,
            honey_kind=apiary.honey_kind,
            organization_id=apiary.organization_id,
        )
        await self.database.execute(query)

    @error_handler
    async def update(self, apiary: ApiaryEntity) -> None:
        data: dict[Any, Any] = {
            "name": apiary.name,
            "location": apiary.location,
            "honey_kind": apiary.honey_kind,
        }
        query = update(orm.apiary_table).values(data).where(orm.apiary_table.c.public_id == apiary.public_id)
        await self.database.execute(query)

    @error_handler
    async def list(self, organization_id: UUID) -> list[ApiaryEntity]:
        query = (
            select(ApiaryEntity)
            .join_from(orm.apiary_table, orm.hive_table, isouter=True)
            .where(orm.apiary_table.c.organization_id == organization_id)
        )
        result = await self.database.execute(query)
        return result.unique().scalars().all()

    @error_handler
    async def delete(self, apiary: ApiaryEntity) -> None:
        query = delete(orm.apiary_table).where(orm.apiary_table.c.public_id == apiary.public_id)
        await self.database.execute(query)
