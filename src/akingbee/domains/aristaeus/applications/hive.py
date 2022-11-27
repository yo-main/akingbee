from akingbee.domains.aristaeus.adapters.repositories.apiary import (
    ApiaryRepositoryAdapter,
)
from akingbee.domains.aristaeus.adapters.repositories.hive import HiveRepositoryAdapter
from akingbee.domains.aristaeus.adapters.repositories.swarm import (
    SwarmRepositoryAdapter,
)
from akingbee.domains.aristaeus.commands.create_hive import CreateHiveCommand
from akingbee.domains.aristaeus.entities.hive import HiveEntity
from akingbee.injector import InjectorMixin


class HiveApplication(InjectorMixin):
    hive_repository: HiveRepositoryAdapter
    apiary_repository: ApiaryRepositoryAdapter

    async def create(self, command: CreateHiveCommand) -> HiveEntity:
        hive = HiveEntity(
            name=command.name,
            condition=command.condition,
            owner_id=command.owner_id,
            apiary_id=command.apiary_id,
            organization_id=command.organization_id,
        )
        await self.hive_repository.save(hive)
        return hive
