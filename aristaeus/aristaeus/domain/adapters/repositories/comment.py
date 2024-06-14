from typing import TYPE_CHECKING
from typing import Protocol
from uuid import UUID

from aristaeus.domain.entities.comment import Comment

__all__ = ["CommentRepositoryAdapter"]


if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class CommentRepositoryAdapter(Base):
    async def save(self, comment: Comment) -> None:
        ...

    async def get(self, public_id: UUID) -> Comment:
        ...

    async def update(self, comment: Comment) -> None:
        ...

    async def delete(self, comment: Comment) -> None:
        ...

    async def list(self, hive_id: UUID) -> list[Comment]:
        ...
