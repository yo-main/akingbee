from typing import List
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from aristaeus.domain.entities.hive import DetailedHiveEntity
from aristaeus.domain.entities.hive import HiveEntity

from .base import BaseModel


class HiveModel(BaseModel):
    public_id: Mapped[UUID] = mapped_column(unique=True)
    name: Mapped[str]
    condition: Mapped[str]
    owner: Mapped[str]
    organization_id: Mapped[UUID]
    swarm_id: Mapped[int | None] = mapped_column(ForeignKey("swarm.id"))
    apiary_id: Mapped[int | None] = mapped_column(ForeignKey("apiary.id"))

    swarm: Mapped[Optional["SwarmModel"]] = relationship(back_populates="hive", lazy="joined")
    apiary: Mapped[Optional["ApiaryModel"]] = relationship(back_populates="hives", lazy="joined")
    events: Mapped[List["EventModel"]] = relationship(back_populates="hive", lazy="joined")
    comments: Mapped[List["CommentModel"]] = relationship(back_populates="hive", lazy="joined")

    def to_entity(self) -> HiveEntity:
        return HiveEntity(
            public_id=self.public_id,
            name=self.name,
            condition=self.condition,
            owner=self.owner,
            organization_id=self.organization_id,
            swarm_id=self.swarm.public_id if self.swarm else None,
            apiary_id=self.apiary.public_id if self.apiary else None,
        )

    def to_detailed_entity(self) -> DetailedHiveEntity:
        return DetailedHiveEntity(
            public_id=self.public_id,
            name=self.name,
            condition=self.condition,
            owner=self.owner,
            swarm=self.swarm.to_entity() if self.swarm else None,
            apiary=self.apiary.to_entity() if self.apiary else None,
        )
