from uuid import UUID

from sqlalchemy import select

from akingbee.domains.aristaeus.adapters.repositories.apiary import (
    ApiaryRepositoryAdapter,
)
from akingbee.domains.aristaeus.entities.apiary import ApiaryEntity
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.models.apiary import ApiaryModel
from akingbee.infrastructure.db.utils import error_handler
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
    async def list(self, organization_id: UUID) -> list[ApiaryEntity]:
        query = select(ApiaryModel).where(ApiaryModel.organization_id == organization_id)
        result = await self.database.execute(query)
        return [model.to_entity() for model in result.scalars()]

    @error_handler
    async def save(self, entity: ApiaryEntity) -> None:
        model = ApiaryModel.from_entity(entity)
        await self.database.save(model, commit=True)
