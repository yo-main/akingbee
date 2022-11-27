from akingbee.domains.aristaeus.adapters.repositories.comment import CommentRepositoryAdapter
from akingbee.domains.aristaeus.commands.create_comment import CreateCommentCommand
from akingbee.domains.aristaeus.entities.comment import CommentEntity
from akingbee.domains.aristaeus.entities.vo.reference import Reference
from akingbee.injector import InjectorMixin


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
