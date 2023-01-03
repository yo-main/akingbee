from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from aristaeus.domain.entities.hive import HiveEntity

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class HiveRepositoryAdapter(Base):
    async def save(self, hive: HiveEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> HiveEntity:
        ...

    async def update(self, hive: HiveEntity, fields: list[str]) -> HiveEntity:
        ...

    async def delete(self, hive: HiveEntity) -> None:
        ...

    async def list(self, organization_id: UUID) -> list[HiveEntity]:
        ...