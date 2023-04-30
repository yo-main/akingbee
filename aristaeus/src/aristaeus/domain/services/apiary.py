from uuid import UUID

from aristaeus.domain.commands.apiary import CreateApiaryCommand
from aristaeus.domain.commands.apiary import PutApiaryCommand
from aristaeus.domain.entities.apiary import Apiary
from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.injector import InjectorMixin


class ApiaryService(InjectorMixin):
    async def create(self, command: CreateApiaryCommand) -> Apiary:
        apiary = Apiary(
            name=command.name,
            location=command.location,
            honey_kind=command.honey_kind,
            organization_id=command.organization_id,
        )
        async with UnitOfWork() as uow:
            await uow.apiary.save(apiary)
            await uow.commit()
        return apiary

    async def put(self, command: PutApiaryCommand) -> Apiary:
        async with UnitOfWork() as uow:
            apiary = await uow.apiary.get(command.apiary_id)

            if name := command.name:
                apiary.rename(name)
            if location := command.location:
                apiary.change_location(location)
            if honey_kind := command.honey_kind:
                apiary.change_honey_kind(honey_kind)

            await uow.apiary.update(apiary=apiary)
            await uow.commit()

        return apiary

    async def delete(self, apiary_id: UUID) -> None:
        async with UnitOfWork() as uow:
            apiary = await uow.apiary.get(apiary_id)
            await uow.apiary.delete(apiary)
            await uow.commit()
