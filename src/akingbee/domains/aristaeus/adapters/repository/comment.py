from typing import Protocol

from domains.bee.entities.comment import CommentEntity
from domains.bee.entities.vo.reference import Reference


class CommentRepositoryAdapter(Protocol):
    async def save_async(self, entity: CommentEntity) -> None:
        ...

    async def get_async(self, reference: Reference) -> CommentEntity:
        ...
