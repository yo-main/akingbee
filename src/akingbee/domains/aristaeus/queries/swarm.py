from uuid import UUID
from akb.domains.bee.adapters.repository.swarm import SwarmRepositoryAdapter
from akb.domains.bee.entities.vo.reference import Reference
from akb.domains.bee.entities.swarm import SwarmEntity

from akb.injector import InjectorMixin


class SwarmQuery(InjectorMixin):
    swarm_repository: SwarmRepositoryAdapter

    async def get_swarm_query(self, swarm_id: UUID) -> SwarmEntity:
        return await self.swarm_repository.get_async(Reference.of(swarm_id))
