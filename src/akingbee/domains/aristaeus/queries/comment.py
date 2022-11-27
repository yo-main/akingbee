from uuid import UUID
from akingbee.domains.aristaeus.entities.comment import CommentEntity
from akingbee.infrastructure.db.repositories.comment import CommentRepositoryAdapter

from akingbee.injector import InjectorMixin


class CommentQuery(InjectorMixin):
    comment_repository: CommentRepositoryAdapter

    async def get_comment_query(self, comment_id: UUID) -> CommentEntity:
        return await self.comment_repository.get(comment_id)
