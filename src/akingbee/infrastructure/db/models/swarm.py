from uuid import UUID

from domains.bee.entities.swarm import SwarmEntity
from domains.bee.entities.vo.reference import Reference
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class SwarmModel(BaseModel):
    health: Mapped[str]
    queen_year: Mapped[int]
    public_id: Mapped[UUID]

    def to_entity(self) -> SwarmEntity:
        return SwarmEntity(
            health=self.health,
            queen_year=self.queen_year,
            public_id=Reference.of(self.public_id),
        )

    @staticmethod
    def from_entity(entity: SwarmEntity) -> "SwarmModel":
        return SwarmModel(health=entity.health, queen_year=entity.queen_year, public_id=entity.public_id.get())
