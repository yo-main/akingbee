from uuid import UUID

from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.domain.entities.swarm import Swarm
from aristaeus.injector import InjectorMixin


class SwarmQuery(InjectorMixin):
    async def get_swarm(self, swarm_id: UUID) -> Swarm:
        async with UnitOfWork() as uow:
            return await uow.swarm.get(swarm_id)
