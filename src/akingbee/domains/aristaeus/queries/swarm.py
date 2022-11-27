from uuid import UUID

from akingbee.domains.aristaeus.adapters.repositories.swarm import (
    SwarmRepositoryAdapter,
)
from akingbee.domains.aristaeus.entities.swarm import SwarmEntity
from akingbee.injector import InjectorMixin


class SwarmQuery(InjectorMixin):
    swarm_repository: SwarmRepositoryAdapter

    async def get_swarm(self, swarm_id: UUID) -> SwarmEntity:
        return await self.swarm_repository.get(swarm_id)
