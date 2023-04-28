from uuid import UUID

from aristaeus.domain.entities.parameter import Parameter
from aristaeus.infrastructure.db.repositories.parameter import (
    ParameterRepositoryAdapter,
)
from aristaeus.injector import InjectorMixin


class ParameterQuery(InjectorMixin):
    parameter_repository: ParameterRepositoryAdapter

    async def get_parameter(self, parameter_id: UUID) -> Parameter:
        return await self.parameter_repository.get(parameter_id)

    async def list_parameters(self, organization_id: UUID, key: str | None = None) -> list[Parameter]:
        return await self.parameter_repository.list(organization_id, key)
