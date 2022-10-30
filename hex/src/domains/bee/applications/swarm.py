import uuid

from domains.bee.adapters.repository.swarm import SwarmRepositoryAdapter
from domains.bee.commands import CreateSwarmCommand
from domains.bee.entities.swarm import SwarmEntity
from domains.bee.entities.user import UserEntity
from domains.bee.entities.vo.reference import Reference


class SwarmApplication:
    def __init__(self, swarm_repository: SwarmRepositoryAdapter):
        self.swarm_repository = swarm_repository

    async def create_async(self, command: CreateSwarmCommand, user: UserEntity) -> SwarmEntity:
        swarm = SwarmEntity.create(queen_year=command.queen_year, health=command.health_status)
        await self.swarm_repository.save_async(swarm)
        return swarm
