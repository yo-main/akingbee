from uuid import UUID

from aristaeus.domain.adapters.repositories.comment import CommentRepositoryAdapter
from aristaeus.domain.commands.comment import CreateCommentCommand
from aristaeus.domain.commands.comment import PutCommentCommand
from aristaeus.domain.entities.comment import CommentEntity
from aristaeus.injector import InjectorMixin


class CommentApplication(InjectorMixin):
    comment_repository: CommentRepositoryAdapter

    async def create(self, command: CreateCommentCommand) -> CommentEntity:
        comment = CommentEntity(
            body=command.body,
            type=command.type,
            date=command.date,
            hive_id=command.hive_id,
            event_id=command.event_id,
        )
        await self.comment_repository.save(comment)
        return comment

    async def put(self, command: PutCommentCommand) -> CommentEntity:
        comment = await self.comment_repository.get(command.comment_id)
        new_comment, updated_fields = comment.update(
            body=command.body,
            date=command.date,
            type=command.type,
        )

        await self.comment_repository.update(comment=new_comment, fields=updated_fields)
        return new_comment

    async def delete(self, comment_id: UUID) -> None:
        comment = await self.comment_repository.get(comment_id)
        await self.comment_repository.delete(comment)
