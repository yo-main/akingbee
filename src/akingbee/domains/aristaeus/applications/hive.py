from domains.bee.adapters.repository.apiary import ApiaryRepositoryAdapter
from domains.bee.adapters.repository.hive import HiveRepositoryAdapter
from domains.bee.adapters.repository.swarm import SwarmRepositoryAdapter
from domains.bee.commands.create_hive import CreateHiveCommand
from domains.bee.entities.hive import HiveEntity
from domains.bee.entities.vo.reference import Reference


class HiveApplication:
    def __init__(
        self,
        hive_repository: HiveRepositoryAdapter,
        apiary_repository: ApiaryRepositoryAdapter,
    ):
        self.hive_repository = hive_repository
        self.apiary_repository = apiary_repository

    async def create_async(self, command: CreateHiveCommand) -> HiveEntity:
        apiary_reference = Reference.of(command.apiary)
        apiary = await self.apiary_repository.get_async(apiary_reference)

        hive = HiveEntity.create(
            name=command.name,
            condition=command.condition,
            owner=command.owner,
            apiary=apiary,
        )
        await self.hive_repository.save_async(hive)
        return hive
