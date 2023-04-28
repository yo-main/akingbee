from uuid import UUID

from aristaeus.domain.adapters.repositories.comment import CommentRepositoryAdapter
from aristaeus.domain.adapters.repositories.hive import HiveRepositoryAdapter
from aristaeus.domain.adapters.repositories.event import EventRepositoryAdapter
from aristaeus.domain.commands.comment import CreateCommentCommand
from aristaeus.domain.commands.comment import PutCommentCommand
from aristaeus.domain.entities.comment import Comment
from aristaeus.injector import InjectorMixin


class CommentApplication(InjectorMixin):
    comment_repository: CommentRepositoryAdapter
    hive_repository: HiveRepositoryAdapter
    event_repository: EventRepositoryAdapter

    async def create(self, command: CreateCommentCommand) -> Comment:
        event = None
        hive = await self.hive_repository.get(command.hive_id)
        if event_id := command.event_id:
            event = await self.event_repository.get(event_id)

        comment = Comment(
            body=command.body,
            type=command.type,
            date=command.date,
            hive=hive,
            event=event,
        )
        await self.comment_repository.save(comment)
        return comment

    async def put(self, command: PutCommentCommand) -> Comment:
        comment = await self.comment_repository.get(command.comment_id)

        if date := command.date:
            comment.change_date(date)
        if body := command.body:
            comment.change_body(body)

        await self.comment_repository.update(comment=comment)
        return comment

    async def delete(self, comment_id: UUID) -> None:
        comment = await self.comment_repository.get(comment_id)
        await self.comment_repository.delete(comment)
