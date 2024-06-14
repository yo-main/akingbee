from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.parameter import Parameter

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class ParameterRepositoryAdapter(Base):
    async def save(self, parameter: Parameter) -> None:
        ...

    async def get(self, parameter_id: UUID) -> Parameter:
        ...
