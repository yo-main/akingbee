from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from sqlalchemy import select

from akingbee.domains.aristaeus.entities.comment import CommentEntity

__all__ = ["CommentRepositoryAdapter"]


if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class CommentRepositoryAdapter(Base):
    async def save(self, entity: CommentEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> CommentEntity:
        ...
