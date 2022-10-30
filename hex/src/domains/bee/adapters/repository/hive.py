from typing import Protocol

from domains.bee.entities.hive import HiveEntity
from domains.bee.entities.vo.reference import Reference


class HiveRepositoryAdapter(Protocol):
    async def save_async(self, hive: HiveEntity) -> None:
        ...

    async def get_async(self, reference: Reference) -> HiveEntity:
        ...
