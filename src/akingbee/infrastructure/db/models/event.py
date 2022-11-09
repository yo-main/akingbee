from datetime import datetime
from uuid import UUID

from domains.bee.entities.event import EventEntity
from domains.bee.entities.vo.reference import Reference
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from .hive import HiveModel


class EventModel(BaseModel):
    public_id: Mapped[UUID]
    hive: Mapped[HiveModel]
    title: Mapped[str]
    description: Mapped[str]
    due_date: Mapped[datetime]
    status: Mapped[str]
    type: Mapped[str]

    def to_entity(self) -> EventEntity:
        return EventEntity(
            public_id=Reference.of(self.public_id),
            hive=self.hive.to_entity(),
            description=self.description,
            due_date=self.due_date,
            status=self.status,
            title=self.title,
            type=self.type,
        )

    @staticmethod
    def from_entity(entity: EventEntity) -> "EventModel":
        return EventModel(
            public_id=entity.public_id.get(),
            hive=HiveModel.from_entity(entity.hive),
            description=entity.description,
            due_date=entity.due_date,
            title=entity.title,
            type=entity.type,
        )
