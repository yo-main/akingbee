from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aristaeus.domain.entities.comment import CommentEntity

from .base import BaseModel


class CommentModel(BaseModel):
    public_id: Mapped[UUID] = mapped_column(unique=True)
    hive_id: Mapped[int] = mapped_column(ForeignKey("hive.id"))
    event_id: Mapped[int | None] = mapped_column(ForeignKey("event.id"))
    date: Mapped[datetime]
    body: Mapped[str]
    type: Mapped[str]

    hive: Mapped["HiveModel"] = relationship(back_populates="comments", lazy="joined")
    event: Mapped[Optional["EventModel"]] = relationship(back_populates="comments", lazy="joined")

    def to_entity(self) -> CommentEntity:
        return CommentEntity(
            public_id=self.public_id,
            date=self.date,
            body=self.body,
            type=self.type,
            event_id=self.event.public_id if self.event else None,
            hive_id=self.hive.public_id,
        )
