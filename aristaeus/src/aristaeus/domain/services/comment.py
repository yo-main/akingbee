from uuid import UUID

from aristaeus.domain.commands.comment import CreateCommentCommand
from aristaeus.domain.commands.comment import PutCommentCommand
from aristaeus.domain.entities.comment import Comment
from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.injector import InjectorMixin


class CommentApplication(InjectorMixin):
    async def create(self, command: CreateCommentCommand) -> Comment:
        async with UnitOfWork() as uow:
            comment = Comment(
                body=command.body, type=command.type, date=command.date, hive=await uow.hive.get(command.hive_id)
            )

            if event_id := command.event_id:
                comment.event = await uow.event.get(event_id)
            await uow.comment.save(comment)
            await uow.commit()

        return comment

    async def put(self, command: PutCommentCommand) -> Comment:
        async with UnitOfWork() as uow:
            comment = await uow.comment.get(command.comment_id)

            if date := command.date:
                comment.change_date(date)
            if body := command.body:
                comment.change_body(body)

            await uow.comment.update(comment=comment)
            await uow.commit()

        return comment

    async def delete(self, comment_id: UUID) -> None:
        async with UnitOfWork() as uow:
            comment = await uow.comment.get(comment_id)
            await uow.comment.delete(comment)
            await uow.commit()
