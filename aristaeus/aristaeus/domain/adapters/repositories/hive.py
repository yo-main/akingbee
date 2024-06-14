from functools import wraps
from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.hive import Hive

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class HiveRepositoryAdapter(Base):
    async def save(self, hive: Hive) -> None:
        ...

    async def get(self, public_id: UUID) -> Hive:
        ...

    async def get_from_swarm_id(self, public_id: UUID) -> Hive:
        ...

    async def update(self, hive: Hive) -> None:
        ...

    async def delete(self, hive: Hive) -> None:
        ...

    async def list(self, organization_id: UUID, with_apiary_only: bool) -> list[Hive]:
        ...
