from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from akingbee.domains.aristaeus.entities.comment import CommentEntity

from .base import BaseModel
from .event import EventModel
from .hive import HiveModel


class CommentModel(BaseModel):
    public_id: Mapped[UUID] = mapped_column(unique=True)
    hive_id: Mapped[UUID]
    event_id: Mapped[UUID | None]
    date: Mapped[datetime]
    body: Mapped[str]
    type: Mapped[str]

    def to_entity(self) -> CommentEntity:
        return CommentEntity(
            public_id=self.public_id,
            date=self.date,
            body=self.body,
            type=self.type,
            event_id=self.event_id,
            hive_id=self.hive_id,
        )

    @staticmethod
    def from_entity(entity: CommentEntity) -> "CommentModel":
        return CommentModel(
            public_id=entity.public_id,
            hive_id=entity.hive_id,
            event_id=entity.event_id,
            body=entity.body,
            date=entity.date,
            type=entity.type,
        )
