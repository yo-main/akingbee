from uuid import UUID

from aristaeus.domain.commands.apiary import CreateApiaryCommand
from aristaeus.domain.commands.apiary import PutApiaryCommand
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

        if name := command.name:
            apiary.rename(name)
        if location := command.location:
            apiary.change_location(location)
        if honey_kind := command.honey_kind:
            apiary.change_honey_kind(honey_kind)

        await self.apiary_repository.update(apiary=apiary)
        return apiary

    async def delete(self, apiary_id: UUID) -> None:
        apiary = await self.apiary_repository.get(apiary_id)
        await self.apiary_repository.delete(apiary)
