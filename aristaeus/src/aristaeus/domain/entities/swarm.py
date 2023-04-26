import uuid
from dataclasses import dataclass
from dataclasses import field
from uuid import UUID

from .base import Entity


@dataclass(slots=True)
class SwarmEntity(Entity):
    health: str
    queen_year: int
    public_id: UUID = field(default_factory=uuid.uuid4)

    def change_health(self, new_health):
        self.health = new_health

    def change_queen_year(self, new_year):
        self.queen_year = new_year

    def __repr__(self):
        return f"<Swarm {self.public_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, SwarmEntity):
            raise ValueError(f"{other} is not a SwarmEntity")
        return self.public_id == other.public_id

    def __hash__(self) -> int:
        return hash(self.public_id)
