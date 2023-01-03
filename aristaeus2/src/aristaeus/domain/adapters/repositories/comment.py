from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from sqlalchemy import select

from aristaeus.domain.entities.comment import CommentEntity

__all__ = ["CommentRepositoryAdapter"]


if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class CommentRepositoryAdapter(Base):
    async def save(self, comment: CommentEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> CommentEntity:
        ...

    async def update(self, comment: CommentEntity, fields: list[str]) -> CommentEntity:
        ...

    async def delete(self, comment: CommentEntity) -> None:
        ...

    async def list(self, hive_id: UUID) -> list[CommentEntity]:
        ...
