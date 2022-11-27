import asyncio
import functools
from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from akingbee.domains.aristaeus.adapters.repositories.parameter import (
    ParameterRepositoryAdapter,
)
from akingbee.domains.aristaeus.entities.parameter import ParameterEntity
from akingbee.domains.aristaeus.errors import EntitySavingError
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.models.parameter import ParameterModel
from akingbee.infrastructure.db.utils import error_handler
from akingbee.injector import Injector
from sqlalchemy import select


@Injector.bind(ParameterRepositoryAdapter)
class ParameterRespository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> ParameterEntity:
        query = select(ParameterModel).where(ParameterModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    @error_handler
    async def save(self, entity: ParameterEntity) -> None:
        model = ParameterModel.from_entity(entity)
        await self.database.save(model, commit=True)
