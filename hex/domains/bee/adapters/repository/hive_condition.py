from typing import Protocol

from domains.bee.entities.hive import HiveConditionEntity
from domains.bee.entities.vo.reference import Reference


class HiveConditionRepositoryAdapter(Protocol):
    def save(self, entity: HiveConditionEntity) -> None:
        ...

    def get(self, reference: Reference) -> HiveConditionEntity:
        ...
