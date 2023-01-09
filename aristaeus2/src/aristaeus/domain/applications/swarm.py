from aristaeus.domain.adapters.repositories.swarm import (
    SwarmRepositoryAdapter,
)
from aristaeus.domain.commands.swarm import CreateSwarmCommand
from aristaeus.domain.entities.swarm import SwarmEntity
from aristaeus.domain.entities.user import UserEntity
from aristaeus.injector import InjectorMixin


class SwarmApplication(InjectorMixin):
    swarm_repository: SwarmRepositoryAdapter

    async def create_swarm(self, command: CreateSwarmCommand, user: UserEntity = None) -> SwarmEntity:
        swarm = SwarmEntity(queen_year=command.queen_year, health=command.health_status)
        await self.swarm_repository.save(swarm)
        return swarm
