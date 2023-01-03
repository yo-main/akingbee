from uuid import UUID

from aristaeus.domain.adapters.repositories.parameter import (
    ParameterRepositoryAdapter,
)
from aristaeus.domain.commands.parameter import (
    CreateParameterCommand,
    PutParameterCommand,
)
from aristaeus.domain.entities.parameter import ParameterEntity
from aristaeus.injector import InjectorMixin


class ParameterApplication(InjectorMixin):
    parameter_repository: ParameterRepositoryAdapter

    async def create(self, command: CreateParameterCommand) -> ParameterEntity:
        parameter = ParameterEntity(
            key=command.key,
            value=command.value,
            organization_id=command.organization_id,
        )
        await self.parameter_repository.save(parameter)
        return parameter

    async def put(self, command: PutParameterCommand) -> ParameterEntity:
        parameter = await self.parameter_repository.get(command.parameter_id)
        new_parameter = await self.parameter_repository.update(parameter=parameter, new_value=command.value)
        return new_parameter

    async def delete(self, public_id: UUID) -> None:
        parameter = await self.parameter_repository.get(public_id)
        await self.parameter_repository.delete(parameter=parameter)
