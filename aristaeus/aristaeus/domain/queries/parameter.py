from uuid import UUID

from aristaeus.domain.entities.parameter import Parameter
from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.injector import InjectorMixin


class ParameterQuery(InjectorMixin):
    async def get_parameter(self, parameter_id: UUID) -> Parameter:
        async with UnitOfWork() as uow:
            return await uow.parameter.get(parameter_id)

    async def list_parameters(self, organization_id: UUID, key: str | None = None) -> list[Parameter]:
        async with UnitOfWork() as uow:
            return await uow.parameter.list(organization_id, key)
