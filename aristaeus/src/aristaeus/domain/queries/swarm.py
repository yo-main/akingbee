from uuid import UUID

from aristaeus.domain.adapters.repositories.swarm import SwarmRepositoryAdapter
from aristaeus.domain.entities.swarm import Swarm
from aristaeus.injector import InjectorMixin


class SwarmQuery(InjectorMixin):
    swarm_repository: SwarmRepositoryAdapter

    async def get_swarm(self, swarm_id: UUID) -> Swarm:
        return await self.swarm_repository.get(swarm_id)
