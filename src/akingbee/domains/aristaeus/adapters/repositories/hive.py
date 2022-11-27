from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from akingbee.domains.aristaeus.entities.hive import HiveEntity

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class HiveRepositoryAdapter(Base):
    async def save(self, hive: HiveEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> HiveEntity:
        ...
