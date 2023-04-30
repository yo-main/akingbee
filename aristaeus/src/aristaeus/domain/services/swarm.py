from uuid import UUID

from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.domain.commands.swarm import CreateSwarmCommand
from aristaeus.domain.commands.swarm import PutSwarmCommand
from aristaeus.domain.entities.swarm import Swarm
from aristaeus.injector import InjectorMixin


class SwarmApplication(InjectorMixin):
    async def create_swarm(self, command: CreateSwarmCommand) -> Swarm:
        swarm = Swarm(queen_year=command.queen_year, health=command.health_status)

        async with UnitOfWork() as uow:
            await uow.swarm.save(swarm)
            await uow.commit()

        return swarm

    async def put(self, command: PutSwarmCommand) -> Swarm:
        async with UnitOfWork() as uow:
            swarm = await uow.swarm.get(command.swarm_id)

            if health := command.health_status:
                swarm.change_health(health)
            if queen_year := command.queen_year:
                swarm.change_queen_year(queen_year)

            await uow.swarm.update(swarm=swarm)
            await uow.commit()

        return swarm

    async def delete_swarm(self, swarm_id: UUID) -> None:
        async with UnitOfWork() as uow:
            swarm = await uow.swarm.get(swarm_id)
            await uow.swarm.delete(swarm)
            await uow.commit()
