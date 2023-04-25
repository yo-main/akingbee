from functools import wraps
from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.hive import HiveEntity

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class HiveRepositoryAdapter(Base):
    async def save(self, hive: HiveEntity) -> None:
        ...

    @wraps(lambda x: 1)
    async def get(self, public_id: UUID) -> HiveEntity:
        ...

    async def update(self, hive: HiveEntity) -> None:
        ...

    async def delete(self, hive: HiveEntity) -> None:
        ...

    async def list(self, organization_id: UUID) -> list[HiveEntity]:
        ...
