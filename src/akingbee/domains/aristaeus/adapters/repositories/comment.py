from sqlalchemy import select
from typing import Protocol
from typing import TYPE_CHECKING
from uuid import UUID

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
