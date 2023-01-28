from uuid import UUID
from aristaeus.domain.adapters.repositories.swarm import SwarmRepositoryAdapter
from aristaeus.domain.adapters.repositories.hive import HiveRepositoryAdapter
from aristaeus.domain.commands.swarm import CreateSwarmCommand
from aristaeus.domain.commands.swarm import PutSwarmCommand
from aristaeus.domain.entities.swarm import SwarmEntity
from aristaeus.domain.entities.user import UserEntity
from aristaeus.injector import InjectorMixin


class SwarmApplication(InjectorMixin):
    hive_repository: HiveRepositoryAdapter
    swarm_repository: SwarmRepositoryAdapter

    async def create_swarm(self, command: CreateSwarmCommand, user: UserEntity = None) -> SwarmEntity:
        swarm = SwarmEntity(queen_year=command.queen_year, health=command.health_status)
        await self.swarm_repository.save(swarm)
        return swarm

    async def put(self, command: PutSwarmCommand) -> SwarmEntity:
        swarm = await self.swarm_repository.get(command.swarm_id)
        new_swarm, updated_fields = swarm.update(
            health=command.health_status,
            queen_year=command.queen_year,
        )

        result = await self.swarm_repository.update(swarm=new_swarm, fields=updated_fields)
        return result

    async def delete_swarm(self, swarm_id: UUID, user: UserEntity = None) -> None:
        swarm = await self.swarm_repository.get(swarm_id)
        await self.swarm_repository.delete(swarm)
