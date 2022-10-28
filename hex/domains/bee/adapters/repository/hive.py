from typing import Protocol

from domains.bee.entities.hive import HiveEntity
from domains.bee.entities.vo.reference import Reference


class HiveRepositoryAdapter(Protocol):
    def create(self, hive: HiveEntity) -> None:
        ...

    def get(self, reference: Reference) -> HiveEntity:
        ...
