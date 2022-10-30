from typing import Protocol

from domains.bee.entities.swarm import SwarmEntity
from domains.bee.entities.vo.reference import Reference


class SwarmRepositoryAdapter(Protocol):
    async def save_async(self, entity: SwarmEntity) -> None:
        ...

    async def get_async(self, reference: Reference) -> SwarmEntity:
        ...
