from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from aristaeus.domain.entities.parameter import ParameterEntity

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class ParameterRepositoryAdapter(Base):
    async def save(self, parameter: ParameterEntity) -> None:
        ...

    async def get(self, parameter_id: UUID) -> ParameterEntity:
        ...
