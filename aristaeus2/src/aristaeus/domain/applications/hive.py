from uuid import UUID

from aristaeus.domain.adapters.repositories.apiary import ApiaryRepositoryAdapter
from aristaeus.domain.adapters.repositories.hive import HiveRepositoryAdapter
from aristaeus.domain.adapters.repositories.swarm import SwarmRepositoryAdapter
from aristaeus.domain.commands.hive import CreateHiveCommand
from aristaeus.domain.commands.hive import PutHiveCommand
from aristaeus.domain.entities.hive import HiveEntity
from aristaeus.injector import InjectorMixin


class HiveApplication(InjectorMixin):
    hive_repository: HiveRepositoryAdapter
    apiary_repository: ApiaryRepositoryAdapter

    async def create(self, command: CreateHiveCommand) -> HiveEntity:
        hive = HiveEntity(
            name=command.name,
            condition=command.condition,
            owner=command.owner,
            apiary_id=command.apiary_id,
            swarm_id=command.swarm_id,
            organization_id=command.organization_id,
        )
        await self.hive_repository.save(hive)
        return hive

    async def put(self, command: PutHiveCommand) -> HiveEntity:
        hive = await self.hive_repository.get(command.hive_id)
        new_hive, updated_fields = hive.update(
            name=command.name, condition=command.condition, owner=command.owner, apiary_id=command.apiary_id
        )

        await self.hive_repository.update(hive=new_hive, fields=updated_fields)
        return new_hive

    async def delete(self, hive_id: UUID) -> None:
        hive = await self.hive_repository.get(hive_id)
        await self.hive_repository.delete(hive)
