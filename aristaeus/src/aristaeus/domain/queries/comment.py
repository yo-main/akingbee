from uuid import UUID

from aristaeus.domain.entities.comment import Comment
from aristaeus.infrastructure.db.repositories.comment import CommentRepositoryAdapter
from aristaeus.injector import InjectorMixin


class CommentQuery(InjectorMixin):
    comment_repository: CommentRepositoryAdapter

    async def get_comment_query(self, comment_id: UUID) -> Comment:
        return await self.comment_repository.get(comment_id)

    async def list_comment_query(self, hive_id: UUID) -> list[Comment]:
        return await self.comment_repository.list(hive_id)
