from datetime import datetime
from uuid import UUID

from domains.bee.entities.comment import CommentEntity
from domains.bee.entities.vo.reference import Reference
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from .hive import HiveModel
from .event import EventModel


class CommentModel(BaseModel):
    public_id: Mapped[UUID]
    hive: Mapped[HiveModel]
    event: Mapped[EventModel]
    date: Mapped[datetime]
    body: Mapped[str]
    status: Mapped[str]
    type: Mapped[str]

    def to_entity(self) -> CommentEntity:
        return CommentEntity(
            public_id=Reference.of(self.public_id),
            hive=self.hive.to_entity(),
            date=self.date,
            body=self.body,
            type=self.type,
            event=self.event.to_entity() if self.event else None,
        )

    @staticmethod
    def from_entity(entity: CommentEntity) -> "CommentModel":
        return CommentModel(
            public_id=entity.public_id.get(),
            hive=HiveModel.from_entity(entity.hive),
            event=EventModel.from_entity(entity.event) if entity.event else None,
            body=entity.body,
            date=entity.date,
            type=entity.type,
        )
