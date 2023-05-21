from uuid import UUID

from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.domain.commands.hive import CreateHiveCommand
from aristaeus.domain.commands.hive import PutHiveCommand
from aristaeus.domain.commands.hive import MoveHiveCommand
from aristaeus.domain.entities.hive import Hive
from aristaeus.injector import InjectorMixin


class HiveService(InjectorMixin):
    async def create(self, command: CreateHiveCommand) -> Hive:
        hive = Hive(
            name=command.name,
            condition=command.condition,
            owner=command.owner,
            organization_id=command.organization_id,
        )

        async with UnitOfWork() as uow:
            if apiary_id := command.apiary_id:
                apiary = await uow.apiary.get(apiary_id)
                hive.move(apiary)
            if swarm_id := command.swarm_id:
                swarm = await uow.swarm.get(swarm_id)
                hive.attach_swarm(swarm)
            await uow.hive.save(hive)
            await uow.commit()

        return hive

    async def put(self, command: PutHiveCommand) -> Hive:
        async with UnitOfWork() as uow:
            hive = await uow.hive.get(command.hive_id)

            if owner := command.owner:
                hive.transfer_ownership(owner)

            if condition := command.condition:
                hive.update_condition(condition)

            if name := command.name:
                hive.rename(name)

            if swarm_id := command.swarm_id:
                swarm = await uow.swarm.get(swarm_id)
                hive.attach_swarm(swarm)

            await uow.hive.update(hive=hive)
            await uow.commit()

        return hive

    async def move_hive(self, command: MoveHiveCommand) -> Hive:
        async with UnitOfWork() as uow:
            hive = await uow.hive.get(command.hive_id)
            apiary = await uow.apiary.get(command.apiary_id)

            hive.move(apiary)

            await uow.hive.update(hive=hive)
            await uow.commit()
        return hive

    async def delete(self, hive_id: UUID) -> None:
        async with UnitOfWork() as uow:
            hive = await uow.hive.get(hive_id)
            await uow.hive.delete(hive)
            await uow.commit()

    async def remove_apiary(self, hive_id: UUID) -> Hive:
        async with UnitOfWork() as uow:
            hive = await uow.hive.get(hive_id)
            hive.remove_apiary()
            await uow.hive.update(hive=hive)
            await uow.commit()

        return hive
