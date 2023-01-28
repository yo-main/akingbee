from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.swarm import SwarmEntity

__all__ = ["SwarmRepositoryAdapter"]


if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class SwarmRepositoryAdapter(Base):
    async def save(self, entity: SwarmEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> SwarmEntity:
        ...

    async def update(self, swarm: SwarmEntity, fields: list[str]) -> SwarmEntity:
        ...

    async def delete(self, swarm: SwarmEntity) -> None:
        ...
