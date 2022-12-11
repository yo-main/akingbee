from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from akingbee.domains.aristaeus.entities.event import EventEntity

from .base import BaseModel


class EventModel(BaseModel):
    public_id: Mapped[UUID] = mapped_column(unique=True)
    hive_id: Mapped[UUID]
    title: Mapped[str]
    description: Mapped[str]
    due_date: Mapped[datetime]
    status: Mapped[str]
    type: Mapped[str]

    def to_entity(self) -> EventEntity:
        return EventEntity(
            public_id=self.public_id,
            hive_id=self.hive_id,
            description=self.description,
            due_date=self.due_date,
            status=self.status,
            title=self.title,
            type=self.type,
        )

    @staticmethod
    def from_entity(entity: EventEntity) -> "EventModel":
        return EventModel(
            public_id=entity.public_id,
            hive_id=entity.hive_id,
            description=entity.description,
            due_date=entity.due_date,
            status=entity.status,
            title=entity.title,
            type=entity.type,
        )
