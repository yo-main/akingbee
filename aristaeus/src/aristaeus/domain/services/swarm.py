from uuid import UUID

from aristaeus.domain.adapters.repositories.hive import HiveRepositoryAdapter
from aristaeus.domain.adapters.repositories.swarm import SwarmRepositoryAdapter
from aristaeus.domain.commands.swarm import CreateSwarmCommand
from aristaeus.domain.commands.swarm import PutSwarmCommand
from aristaeus.domain.entities.swarm import Swarm
from aristaeus.injector import InjectorMixin


class SwarmApplication(InjectorMixin):
    hive_repository: HiveRepositoryAdapter
    swarm_repository: SwarmRepositoryAdapter

    async def create_swarm(self, command: CreateSwarmCommand) -> Swarm:
        swarm = Swarm(queen_year=command.queen_year, health=command.health_status)
        await self.swarm_repository.save(swarm)
        return swarm

    async def put(self, command: PutSwarmCommand) -> Swarm:
        swarm = await self.swarm_repository.get(command.swarm_id)

        if health := command.health_status:
            swarm.change_health(health)
        if queen_year := command.queen_year:
            swarm.change_queen_year(queen_year)

        await self.swarm_repository.update(swarm=swarm)
        return swarm

    async def delete_swarm(self, swarm_id: UUID) -> None:
        swarm = await self.swarm_repository.get(swarm_id)
        await self.swarm_repository.delete(swarm)
