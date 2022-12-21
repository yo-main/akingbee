from typing import List, Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from akingbee.domains.aristaeus.entities.hive import HiveEntity

from .base import BaseModel

# from akingbee.infrastructure.db.models.apiary import ApiaryModel
# from akingbee.infrastructure.db.models.swarm import SwarmModel



class HiveModel(BaseModel):
    public_id: Mapped[UUID] = mapped_column(unique=True)
    name: Mapped[str]
    condition: Mapped[str]
    owner_id: Mapped[UUID]
    organization_id: Mapped[UUID]
    swarm_id: Mapped[int | None] = mapped_column(ForeignKey("swarm.id"))
    apiary_id: Mapped[int | None] = mapped_column(ForeignKey("apiary.id"))

    swarm: Mapped[Optional["SwarmModel"]] = relationship(back_populates="hive", lazy="joined")
    apiary: Mapped[Optional["ApiaryModel"]] = relationship(back_populates="hive", lazy="joined")
    events: Mapped[List["EventModel"]] = relationship(back_populates="hive", lazy="joined")
    comments: Mapped[List["CommentModel"]] = relationship(back_populates="hive", lazy="joined")

    def to_entity(self) -> HiveEntity:
        return HiveEntity(
            public_id=self.public_id,
            name=self.name,
            condition=self.condition,
            owner_id=self.owner_id,
            organization_id=self.organization_id,
            swarm_id=self.swarm.public_id if self.swarm else None,
            apiary_id=self.apiary.public_id if self.apiary else None,
        )
