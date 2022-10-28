from domains.bee.adapters.repository.comment import CommentRepositoryAdapter
from domains.bee.adapters.repository.event import EventRepositoryAdapter
from domains.bee.adapters.repository.hive import HiveRepositoryAdapter
from domains.bee.commands.create_comment import CreateCommentCommand
from domains.bee.entities.comment import CommentEntity
from domains.bee.entities.vo.reference import Reference


class CommentApplication:
    def __init__(
        self,
        comment_repository: CommentRepositoryAdapter,
        event_repository: EventRepositoryAdapter,
        hive_repository: HiveRepositoryAdapter,
    ):
        self.comment_repository = comment_repository
        self.hive_repository = hive_repository
        self.event_repository = event_repository

    def create(self, command: CreateCommentCommand) -> CommentEntity:
        hive_reference = Reference.of(command.hive)
        hive = self.hive_repository.get(hive_reference)
        event = None
        if command.event:
            event_reference = Reference.of(command.event)
            event = self.event_repository.get(event_reference)

        comment = CommentEntity.create(
            body=command.body,
            type=command.type,
            date=command.date,
            hive=hive,
            event=event,
        )
        self.comment_repository.save(comment)
        return comment
