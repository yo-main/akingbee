from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.harvest import Harvest

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class HarvestRepositoryAdapter(Base):
    async def save(self, harvest: Harvest) -> None:
        ...

    async def list(self, hive_id: UUID) -> list[Harvest]:
        ...
