from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload

from aristaeus.domain.adapters.repositories.apiary import ApiaryRepositoryAdapter
from aristaeus.domain.entities.apiary import ApiaryEntity
from aristaeus.domain.entities.apiary import DetailedApiaryEntity
from aristaeus.infrastructure.db.engine import AsyncDatabase
from aristaeus.infrastructure.db.models.apiary import ApiaryModel
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.injector import Injector


@Injector.bind(ApiaryRepositoryAdapter)
class ApiaryRespository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> ApiaryEntity:
        query = select(ApiaryModel).options(joinedload(ApiaryModel.hives)).where(ApiaryModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.unique().scalar_one().to_entity()

    @error_handler
    async def save(self, apiary: ApiaryEntity) -> None:
        model = ApiaryModel.from_entity(apiary)
        query = insert(ApiaryModel).values(model.to_dict())
        await self.database.execute(query)

    @error_handler
    async def update(self, apiary: ApiaryEntity, fields: list[str]) -> ApiaryEntity:
        query = (
            update(ApiaryModel)
            .values({field: getattr(apiary, field) for field in fields})
            .where(ApiaryModel.public_id == apiary.public_id)
        )
        await self.database.execute(query)
        return await self.get(apiary.public_id)

    @error_handler
    async def list(self, organization_id: UUID) -> list[DetailedApiaryEntity]:
        query = (
            select(ApiaryModel)
            .options(joinedload(ApiaryModel.hives))
            .where(ApiaryModel.organization_id == organization_id)
        )
        result = await self.database.execute(query)
        return [model.to_detailed_entity() for model in result.unique().scalars()]

    @error_handler
    async def delete(self, apiary: ApiaryEntity) -> None:
        query = delete(ApiaryModel).where(ApiaryModel.public_id == apiary.public_id)
        await self.database.execute(query)
