from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aristaeus.domain.entities.user import UserEntity

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class UserRepositoryAdapter(Base):
    async def save(self, user: UserEntity, session: AsyncSession | None) -> None:
        ...

    async def get(self, public_id: UUID) -> UserEntity:
        ...
