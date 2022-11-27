from akingbee.domains.aristaeus.commands.create_apiary import CreateApiaryCommand
from akingbee.domains.aristaeus.entities.apiary import ApiaryEntity
from akingbee.infrastructure.db.repositories.apiary import ApiaryRepositoryAdapter
from akingbee.injector import InjectorMixin


class ApiaryApplication(InjectorMixin):
    apiary_repository: ApiaryRepositoryAdapter

    async def create(self, command: CreateApiaryCommand) -> ApiaryEntity:
        apiary = ApiaryEntity(
            name=command.name,
            location=command.location,
            honey_kind=command.honey_kind,
            organization_id=command.organization_id,
        )
        await self.apiary_repository.save(apiary)
        return apiary
