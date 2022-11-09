from typing import Protocol
from typing import TYPE_CHECKING

from akingbee.domains.aristaeus.entities.swarm import SwarmEntity
from akingbee.domains.aristaeus.entities.vo.reference import Reference

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class SwarmRepositoryAdapter(Base):
    async def save_async(self, entity: SwarmEntity) -> None:
        ...

    async def get_async(self, reference: Reference) -> SwarmEntity:
        ...
