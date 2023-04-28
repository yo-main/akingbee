from uuid import UUID

from aristaeus.domain.adapters.repositories.apiary import ApiaryRepositoryAdapter
from aristaeus.domain.adapters.repositories.hive import HiveRepositoryAdapter
from aristaeus.domain.adapters.repositories.swarm import SwarmRepositoryAdapter
from aristaeus.domain.commands.hive import CreateHiveCommand
from aristaeus.domain.commands.hive import PutHiveCommand
from aristaeus.domain.commands.hive import MoveHiveCommand
from aristaeus.domain.entities.hive import Hive
from aristaeus.injector import InjectorMixin


class HiveApplication(InjectorMixin):
    hive_repository: HiveRepositoryAdapter
    apiary_repository: ApiaryRepositoryAdapter
    swarm_repository: SwarmRepositoryAdapter

    async def create(self, command: CreateHiveCommand) -> Hive:
        apiary = swarm = None

        if apiary_id := command.apiary_id:
            apiary = await self.apiary_repository.get(apiary_id)
        if swarm_id := command.swarm_id:
            swarm = await self.swarm_repository.get(swarm_id)

        hive = Hive(
            name=command.name,
            condition=command.condition,
            owner=command.owner,
            apiary=apiary,
            swarm=swarm,
            organization_id=command.organization_id,
        )
        await self.hive_repository.save(hive)
        return hive

    async def put(self, command: PutHiveCommand) -> Hive:
        hive = await self.hive_repository.get(command.hive_id)

        if owner := command.owner:
            hive.transfer_ownership(owner)

        if condition := command.condition:
            hive.update_condition(condition)

        if name := command.name:
            hive.rename(name)

        if swarm_id := command.swarm_id:
            swarm = await self.swarm_repository.get(swarm_id)
            hive.attach_swarm(swarm)

        await self.hive_repository.update(hive=hive)
        return hive

    async def move_hive(self, command: MoveHiveCommand) -> Hive:
        hive = await self.hive_repository.get(command.hive_id)
        apiary = await self.apiary_repository.get(command.apiary_id)

        hive.move(apiary)

        await self.hive_repository.update(hive=hive)
        return hive

    async def delete(self, hive_id: UUID) -> None:
        hive = await self.hive_repository.get(hive_id)
        await self.hive_repository.delete(hive)
