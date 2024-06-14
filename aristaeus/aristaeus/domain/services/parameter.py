from uuid import UUID

from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.domain.commands.parameter import CreateParameterCommand
from aristaeus.domain.commands.parameter import PutParameterCommand
from aristaeus.domain.entities.parameter import Parameter
from aristaeus.injector import InjectorMixin


class ParameterApplication(InjectorMixin):
    async def create(self, command: CreateParameterCommand) -> Parameter:
        parameter = Parameter(
            key=command.key,
            value=command.value,
            organization_id=command.organization_id,
        )
        async with UnitOfWork() as uow:
            await uow.parameter.save(parameter)
            await uow.commit()

        return parameter

    async def put(self, command: PutParameterCommand) -> Parameter:
        async with UnitOfWork() as uow:
            parameter = await uow.parameter.get(command.parameter_id)
            parameter.change_value(command.value)

            await uow.parameter.update(parameter=parameter)
            await uow.commit()

        return parameter

    async def delete(self, public_id: UUID) -> None:
        async with UnitOfWork() as uow:
            parameter = await uow.parameter.get(public_id)
            await uow.parameter.delete(parameter=parameter)
            await uow.commit()
