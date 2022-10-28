from typing import Protocol

from domains.bee.entities.comment import CommentEntity
from domains.bee.entities.vo.reference import Reference


class CommentRepositoryAdapter(Protocol):
    def save(self, entity: CommentEntity) -> None:
        ...

    def get(self, reference: Reference) -> CommentEntity:
        ...
