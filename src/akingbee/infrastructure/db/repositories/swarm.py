import asyncio
import functools
from sqlalchemy import select
from typing import Protocol
from typing import TYPE_CHECKING
from uuid import UUID

from akingbee.domains.aristaeus.entities.swarm import SwarmEntity
from akingbee.domains.aristaeus.errors import EntitySavingError
from akingbee.infrastructure.db.utils import error_handler
from akingbee.infrastructure.db.models.swarm import SwarmModel
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.injector import Injector

from akingbee.domains.aristaeus.adapters.repositories.swarm import SwarmRepositoryAdapter


@Injector.bind(SwarmRepositoryAdapter)
class SwarmRespository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> SwarmEntity:
        query = select(SwarmModel).where(SwarmModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    @error_handler
    async def save(self, entity: SwarmEntity) -> None:
        model = SwarmModel.from_entity(entity)
        await self.database.save(model, commit=True)
