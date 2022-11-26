from akingbee.domains.aristaeus.commands.create_swarm import CreateSwarmCommand
from akingbee.domains.aristaeus.entities.swarm import SwarmEntity
from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.domains.aristaeus.applications.base import BaseApplication
from akingbee.domains.aristaeus.adapters.repositories.swarm import SwarmRepositoryAdapter

from akingbee.injector import InjectorMixin


class SwarmApplication(InjectorMixin):
    swarm_repository: SwarmRepositoryAdapter

    async def create_swarm(self, command: CreateSwarmCommand, user: UserEntity = None) -> SwarmEntity:
        swarm = SwarmEntity(queen_year=command.queen_year, health=command.health_status)
        await self.swarm_repository.save(swarm)
        return swarm
