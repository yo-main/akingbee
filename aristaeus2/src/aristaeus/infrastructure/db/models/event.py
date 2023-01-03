from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aristaeus.domain.entities.event import EventEntity

from .base import BaseModel


class EventModel(BaseModel):
    public_id: Mapped[UUID] = mapped_column(unique=True)
    hive_id: Mapped[int] = mapped_column(ForeignKey("hive.id"))
    title: Mapped[str]
    description: Mapped[str]
    due_date: Mapped[datetime]
    status: Mapped[str]
    type: Mapped[str]

    hive: Mapped["HiveModel"] = relationship(back_populates="events", lazy="joined")
    comments: Mapped[List["CommentModel"]] = relationship(back_populates="event")

    def to_entity(self) -> EventEntity:
        return EventEntity(
            public_id=self.public_id,
            hive_id=self.hive.public_id,
            description=self.description,
            due_date=self.due_date,
            status=self.status,
            title=self.title,
            type=self.type,
        )
