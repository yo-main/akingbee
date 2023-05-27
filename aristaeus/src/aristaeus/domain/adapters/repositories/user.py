from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.user import User

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class UserRepositoryAdapter(Base):
    async def save(self, user: User) -> None:
        ...

    async def get(self, public_id: UUID) -> User:
        ...
