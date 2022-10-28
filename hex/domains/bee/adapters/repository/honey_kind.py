from typing import Protocol

from domains.bee.entities.apiary import HoneyKindEntity
from domains.bee.entities.vo.reference import Reference


class HoneyKindRepositoryAdapter(Protocol):
    def save(self, apiary: HoneyKindEntity) -> None:
        ...

    def get(self, reference: Reference) -> HoneyKindEntity:
        ...
