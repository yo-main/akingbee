import uuid

from infrastruture.db.repositories.swarm import SwarmRepository

from domains.bee.adapters.repository.swarm import SwarmRepositoryAdapter
from domains.bee.adapters.repository.swarm_health import SwarmHealthRepositoryAdapter
from domains.bee.adapters.repository.user import UserRepositoryAdapter
from domains.bee.commands import CreateSwarmCommand
from domains.bee.entities.swarm import SwarmEntity
from domains.bee.entities.user import UserEntity
from domains.bee.entities.vo.reference import Reference
from domains.bee.errors import EntityNotFound, EntityPersistError


class SwarmApplication:
    def __init__(self, swarm_repository: SwarmRepositoryAdapter):
        self.swarm_repository = swarm_repository

    def create_swarm(self, command: CreateSwarmCommand, user: UserEntity) -> SwarmEntity:
        swarm = SwarmEntity.create(queen_year=command.queen_year, health=command.health_status)
        self.swarm_repository.save(swarm)
        return swarm
