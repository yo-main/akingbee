from domains.bee.adapters.repository.apiary import ApiaryRepositoryAdapter
from domains.bee.commands.create_apiary import CreateApiaryCommand
from domains.bee.entities.apiary import ApiaryEntity
from domains.bee.entities.vo.reference import Reference


class ApiaryApplication:
    def __init__(self, apiary_repository: ApiaryRepositoryAdapter):
        self.apiary_repository = apiary_repository

    async def create_async(self, command: CreateApiaryCommand) -> ApiaryEntity:
        apiary = ApiaryEntity.create(name=command.name, location=command.location, honey_kind=command.honey_kind)
        await self.apiary_repository.save_async(apiary)
        return apiary
