from sqlalchemy import select
from typing import Protocol
from typing import TYPE_CHECKING
from uuid import UUID

from akingbee.domains.aristaeus.entities.swarm import SwarmEntity


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
