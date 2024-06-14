from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.apiary import Apiary

__all__ = ["ApiaryRepositoryAdapter"]


if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class ApiaryRepositoryAdapter(Base):
    async def save(self, apiary: Apiary) -> None:
        ...

    async def get(self, public_id: UUID) -> Apiary:
        ...

    async def update(self, apiary: Apiary) -> None:
        ...

    async def list(self, organization_id: UUID) -> list[Apiary]:
        ...

    async def delete(self, apiary: Apiary) -> None:
        ...
