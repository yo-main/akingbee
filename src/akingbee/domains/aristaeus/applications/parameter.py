from akingbee.domains.aristaeus.adapters.repositories.parameter import ParameterRepositoryAdapter
from akingbee.domains.aristaeus.commands.create_parameter import CreateParameterCommand
from akingbee.domains.aristaeus.entities.parameter import ParameterEntity
from akingbee.injector import InjectorMixin


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
