from uuid import UUID

from sqlalchemy import insert, select

from akingbee.domains.aristaeus.adapters.repositories.parameter import (
    ParameterRepositoryAdapter,
)
from akingbee.domains.aristaeus.entities.parameter import ParameterEntity
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.models.parameter import ParameterModel
from akingbee.infrastructure.db.utils import error_handler, get_data_from_entity
from akingbee.injector import Injector


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
        query = insert(ParameterModel).values(data)
        await self.database.execute(query)
