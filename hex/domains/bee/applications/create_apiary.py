from domains.bee.adapters.repository.apiary import ApiaryRepositoryAdapter
from domains.bee.adapters.repository.honey_kind import HoneyKindRepositoryAdapter
from domains.bee.adapters.repository.user import UserRepositoryAdapter
from domains.bee.commands.create_apiary import CreateApiaryCommand
from domains.bee.entities.apiary import ApiaryEntity, HoneyKindEntity
from domains.bee.entities.vo.reference import Reference
from domains.bee.errors import EntityNotFound, EntityPersistError


class ApiaryApplication:
    def __init__(self, apiary_repository: ApiaryRepositoryAdapter):
        self.apiary_repository = apiary_repository

    def create(self, command: CreateApiaryCommand) -> ApiaryEntity:
        apiary = ApiaryEntity.create(name=command.name, location=command.location, honey_kind=command.honey_kind)
        self.apiary_repository.save(apiary)
        return apiary
