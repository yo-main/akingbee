from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from akingbee.domains.aristaeus.entities.swarm import SwarmEntity

from .base import BaseModel


class SwarmModel(BaseModel):
    health: Mapped[str]
    queen_year: Mapped[int]
    public_id: Mapped[UUID] = mapped_column(unique=True)

    def to_entity(self) -> SwarmEntity:
        return SwarmEntity(
            health=self.health,
            queen_year=self.queen_year,
            public_id=self.public_id,
        )

    @staticmethod
    def from_entity(entity: SwarmEntity) -> "SwarmModel":
        return SwarmModel(health=entity.health, queen_year=entity.queen_year, public_id=entity.public_id)
