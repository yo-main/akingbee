from uuid import UUID

from sqlalchemy import delete, insert, select, update

from akingbee.domains.aristaeus.adapters.repositories.apiary import (
    ApiaryRepositoryAdapter,
)
from akingbee.domains.aristaeus.entities.apiary import ApiaryEntity
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.models.apiary import ApiaryModel
from akingbee.infrastructure.db.utils import error_handler, get_data_from_entity
from akingbee.injector import Injector


@Injector.bind(ApiaryRepositoryAdapter)
class ApiaryRespository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> ApiaryEntity:
        query = select(ApiaryModel).where(ApiaryModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    @error_handler
    async def save(self, apiary: ApiaryEntity) -> None:
        data = get_data_from_entity(apiary)
        query = insert(ApiaryModel).values(data)
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
    async def list(self, organization_id: UUID) -> list[ApiaryEntity]:
        query = select(ApiaryModel).where(ApiaryModel.organization_id == organization_id)
        result = await self.database.execute(query)
        return [model.to_entity() for model in result.scalars()]

    @error_handler
    async def delete(self, apiary: ApiaryEntity) -> None:
        query = delete(ApiaryModel).where(ApiaryModel.public_id == apiary.public_id)
        await self.database.execute(query)
