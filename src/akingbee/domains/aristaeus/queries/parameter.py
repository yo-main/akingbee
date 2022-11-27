from uuid import UUID
from akingbee.domains.aristaeus.entities.parameter import ParameterEntity
from akingbee.infrastructure.db.repositories.parameter import ParameterRepositoryAdapter

from akingbee.injector import InjectorMixin


class ParameterQuery(InjectorMixin):
    parameter_repository: ParameterRepositoryAdapter

    async def get_parameter_query(self, parameter_id: UUID) -> ParameterEntity:
        return await self.parameter_repository.get(parameter_id)
