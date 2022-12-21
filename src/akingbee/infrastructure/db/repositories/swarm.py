from uuid import UUID

from sqlalchemy import insert, select

from akingbee.domains.aristaeus.adapters.repositories.swarm import (
    SwarmRepositoryAdapter,
)
from akingbee.domains.aristaeus.entities.swarm import SwarmEntity
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.models.swarm import SwarmModel
from akingbee.infrastructure.db.utils import error_handler, get_data_from_entity
from akingbee.injector import Injector


@Injector.bind(SwarmRepositoryAdapter)
class SwarmRespository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> SwarmEntity:
        query = select(SwarmModel).where(SwarmModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    @error_handler
    async def save(self, swarm: SwarmEntity) -> None:
        data = get_data_from_entity(swarm)
        query = insert(SwarmModel).values(data)
        await self.database.execute(query)
