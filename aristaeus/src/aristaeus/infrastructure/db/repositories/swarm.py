from typing import Any
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from aristaeus.domain.adapters.repositories.swarm import SwarmRepositoryAdapter
from aristaeus.domain.entities.swarm import SwarmEntity
from aristaeus.domain.errors import EntityNotFound
from aristaeus.infrastructure.db.engine import AsyncDatabase
from aristaeus.infrastructure.db.models.swarm import SwarmModel
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.infrastructure.db.utils import get_data_from_entity
from aristaeus.injector import Injector


@Injector.bind(SwarmRepositoryAdapter, "test")
class FakeSwarmRepository:
    _swarms: set[SwarmEntity] = set()

    @error_handler
    async def get(self, public_id: UUID) -> SwarmEntity:
        try:
            return next(swarm for swarm in self._swarms if swarm.public_id == public_id)
        except StopIteration:
            raise EntityNotFound("Swarm not found")

    @error_handler
    async def save(self, swarm: SwarmEntity) -> None:
        self._swarms.add(swarm)

    @error_handler
    async def update(self, swarm: SwarmEntity) -> None:
        self._swarms.discard(swarm)
        self._swarms.add(swarm)

    @error_handler
    async def delete(self, swarm: SwarmEntity) -> None:
        self._swarms.discard(swarm)


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

    @error_handler
    async def update(self, swarm: SwarmEntity) -> None:
        data: dict[Any, Any] = {"queen_year": swarm.queen_year, "health": swarm.health}
        query = update(SwarmModel).values(data).where(SwarmModel.public_id == swarm.public_id)
        await self.database.execute(query)

    @error_handler
    async def delete(self, swarm: SwarmEntity) -> None:
        query = delete(SwarmModel).where(SwarmModel.public_id == swarm.public_id)
        await self.database.execute(query)
