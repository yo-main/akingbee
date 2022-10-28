from typing import Protocol

from domains.bee.entities.swarm import SwarmHealthEntity
from domains.bee.entities.vo.reference import Reference


class SwarmHealthRepositoryAdapter(Protocol):
    def save(self, entity: SwarmHealthEntity) -> None:
        ...

    def get(self, reference: Reference) -> SwarmHealthEntity:
        ...
