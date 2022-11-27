from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from akingbee.domains.aristaeus.entities.swarm import SwarmEntity
from sqlalchemy import select

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
