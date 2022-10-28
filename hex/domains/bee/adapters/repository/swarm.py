from typing import Protocol

from domains.bee.entities.swarm import SwarmEntity
from domains.bee.entities.vo.reference import Reference


class SwarmRepositoryAdapter(Protocol):
    def save(self, entity: SwarmEntity) -> None:
        ...

    def get(self, reference: Reference) -> SwarmEntity:
        ...
