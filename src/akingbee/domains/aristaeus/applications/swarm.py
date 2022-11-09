import uuid

from akb.domains.bee.adapters.repository.swarm import SwarmRepositoryAdapter
from akb.domains.bee.commands.create_swarm import CreateSwarmCommand
from akb.domains.bee.entities.swarm import SwarmEntity
from akb.domains.bee.entities.user import UserEntity
from akb.domains.bee.entities.vo.reference import Reference
from akb.domains.bee.applications.base import BaseApplication

from akb.injector import InjectorMixin


class SwarmApplication(InjectorMixin):
    swarm_repository: SwarmRepositoryAdapter

    async def create_async(self, command: CreateSwarmCommand, user: UserEntity = None) -> SwarmEntity:
        swarm = SwarmEntity.create(queen_year=command.queen_year, health=command.health_status)
        await self.swarm_repository.save_async(swarm)
        return swarm
