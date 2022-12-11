from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from akingbee.domains.aristaeus.entities.apiary import ApiaryEntity

__all__ = ["ApiaryRepositoryAdapter"]


if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class ApiaryRepositoryAdapter(Base):
    async def save(self, entity: ApiaryEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> ApiaryEntity:
        ...

    async def update(self, entity: ApiaryEntity, fields: list[str]) -> list[ApiaryEntity]:
        ...

    async def list(self, organization_id: UUID) -> list[ApiaryEntity]:
        ...

    async def delete(self, entity: ApiaryEntity) -> None:
        ...
