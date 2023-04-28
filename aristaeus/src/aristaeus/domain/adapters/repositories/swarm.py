from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.swarm import Swarm

__all__ = ["SwarmRepositoryAdapter"]


if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class SwarmRepositoryAdapter(Base):
    async def save(self, entity: Swarm) -> None:
        ...

    async def get(self, public_id: UUID) -> Swarm:
        ...

    async def update(self, swarm: Swarm) -> None:
        ...

    async def delete(self, swarm: Swarm) -> None:
        ...
