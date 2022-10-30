from typing import Protocol

from domains.bee.entities.swarm import SwarmHealthEntity
from domains.bee.entities.vo.reference import Reference


class SwarmHealthRepositoryAdapterAsync(Protocol):
    async def save(self, entity: SwarmHealthEntity) -> None:
        ...

    async def get(self, reference: Reference) -> SwarmHealthEntity:
        ...
