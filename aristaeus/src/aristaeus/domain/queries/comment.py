from uuid import UUID

from aristaeus.domain.entities.comment import Comment
from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.injector import InjectorMixin


class CommentQuery(InjectorMixin):
    async def get_comment_query(self, comment_id: UUID) -> Comment:
        async with UnitOfWork() as uow:
            return await uow.comment.get(comment_id)

    async def list_comment_query(self, hive_id: UUID) -> list[Comment]:
        async with UnitOfWork() as uow:
            return await uow.comment.list(hive_id)
