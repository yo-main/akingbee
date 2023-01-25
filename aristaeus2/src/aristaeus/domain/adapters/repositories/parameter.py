from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.parameter import ParameterEntity

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class ParameterRepositoryAdapter(Base):
    async def save(self, parameter: ParameterEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> ParameterEntity:
        ...

    async def update(self, parameter: ParameterEntity, new_value: str) -> ParameterEntity:
        ...

    async def delete(self, parameter: ParameterEntity) -> None:
        ...

    async def list(self, organization_id: UUID, key: str | None = None) -> list[ParameterEntity]:
        ...
