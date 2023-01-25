from uuid import UUID

from aristaeus.domain.commands.apiary import (
    CreateApiaryCommand,
    PutApiaryCommand,
)
from aristaeus.domain.entities.apiary import ApiaryEntity
from aristaeus.infrastructure.db.repositories.apiary import ApiaryRepositoryAdapter
from aristaeus.injector import InjectorMixin


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

    async def put(self, command: PutApiaryCommand) -> ApiaryEntity:
        apiary = await self.apiary_repository.get(command.apiary_id)
        new_apiary, updated_fields = apiary.update(
            name=command.name,
            location=command.location,
            honey_kind=command.honey_kind,
        )

        await self.apiary_repository.update(apiary=new_apiary, fields=updated_fields)
        return new_apiary

    async def delete(self, apiary_id: UUID) -> None:
        apiary = await self.apiary_repository.get(apiary_id)
        await self.apiary_repository.delete(apiary)
