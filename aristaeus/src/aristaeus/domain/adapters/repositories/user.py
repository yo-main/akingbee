from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.user import UserEntity

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class UserRepositoryAdapter(Base):
    async def save(self, user: UserEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> UserEntity:
        ...
