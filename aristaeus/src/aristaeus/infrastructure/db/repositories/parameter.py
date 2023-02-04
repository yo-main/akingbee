from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert

from aristaeus.domain.adapters.repositories.parameter import ParameterRepositoryAdapter
from aristaeus.domain.entities.parameter import ParameterEntity
from aristaeus.infrastructure.db.engine import AsyncDatabase
from aristaeus.infrastructure.db.models.parameter import ParameterModel
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.infrastructure.db.utils import get_data_from_entity
from aristaeus.injector import Injector


@Injector.bind(ParameterRepositoryAdapter)
class ParameterRespository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> ParameterEntity:
        query = select(ParameterModel).where(ParameterModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    @error_handler
    async def save(self, parameter: ParameterEntity) -> None:
        data = get_data_from_entity(parameter)
        query = insert(ParameterModel).values(data).on_conflict_do_nothing()
        await self.database.execute(query)

    @error_handler
    async def update(self, parameter: ParameterEntity, new_value: str) -> ParameterEntity:
        query = (
            update(ParameterModel).values({"value": new_value}).where(ParameterModel.public_id == parameter.public_id)
        )
        await self.database.execute(query)
        return await self.get(parameter.public_id)

    @error_handler
    async def delete(self, parameter: ParameterEntity) -> None:
        query = delete(ParameterModel).where(ParameterModel.public_id == parameter.public_id)
        await self.database.execute(query)

    @error_handler
    async def list(self, organization_id: UUID, key: str | None = None) -> list[ParameterEntity]:
        query = select(ParameterModel).where(ParameterModel.organization_id == organization_id)
        if key is not None:
            query = query.where(ParameterModel.key == key)
        result = await self.database.execute(query)
        return [model.to_entity() for model in result.unique().scalars()]
