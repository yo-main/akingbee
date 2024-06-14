from typing import Any
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from aristaeus.domain.adapters.repositories.swarm import SwarmRepositoryAdapter
from aristaeus.domain.entities.swarm import Swarm
from aristaeus.domain.errors import EntityNotFound
from aristaeus.infrastructure.db import orm
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.injector import Injector

from .base import BaseRepository


@Injector.bind(SwarmRepositoryAdapter, "test")
class FakeSwarmRepository(BaseRepository):
    _swarms: set[Swarm] = set()

    @error_handler()
    async def get(self, public_id: UUID) -> Swarm:
        try:
            return next(swarm for swarm in self._swarms if swarm.public_id == public_id)
        except StopIteration:
            raise EntityNotFound("Swarm not found")

    @error_handler()
    async def save(self, swarm: Swarm) -> None:
        self._swarms.add(swarm)

    @error_handler()
    async def update(self, swarm: Swarm) -> None:
        self._swarms.discard(swarm)
        self._swarms.add(swarm)

    @error_handler()
    async def delete(self, swarm: Swarm) -> None:
        self._swarms.discard(swarm)


@Injector.bind(SwarmRepositoryAdapter)
class SwarmRespository(BaseRepository):
    @error_handler()
    async def get(self, public_id: UUID) -> Swarm:
        query = select(Swarm).where(orm.swarm_table.c.public_id == public_id)
        result = await self.session.execute(query)
        return result.scalar_one()

    @error_handler()
    async def save(self, swarm: Swarm) -> None:
        data = {
            "health": swarm.health,
            "queen_year": swarm.queen_year,
            "public_id": swarm.public_id,
        }
        query = insert(orm.swarm_table).values(data)
        await self.session.execute(query)

    @error_handler()
    async def update(self, swarm: Swarm) -> None:
        data: dict[Any, Any] = {"queen_year": swarm.queen_year, "health": swarm.health}
        query = update(orm.swarm_table).values(data).where(orm.swarm_table.c.public_id == swarm.public_id)
        await self.session.execute(query)

    @error_handler()
    async def delete(self, swarm: Swarm) -> None:
        query = delete(orm.swarm_table).where(orm.swarm_table.c.public_id == swarm.public_id)
        await self.session.execute(query)
