from typing import Protocol
from typing import TYPE_CHECKING

from domains.bee.entities.hive import HiveEntity
from domains.bee.entities.vo.reference import Reference

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class HiveRepositoryAdapter(Base):
    async def save_async(self, hive: HiveEntity) -> None:
        ...

    async def get_async(self, reference: Reference) -> HiveEntity:
        ...
