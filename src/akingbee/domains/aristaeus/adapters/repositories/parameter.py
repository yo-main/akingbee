from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from akingbee.domains.aristaeus.entities.parameter import ParameterEntity

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class ParameterRepositoryAdapter(Base):
    async def save(self, parameter: ParameterEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> ParameterEntity:
        ...
