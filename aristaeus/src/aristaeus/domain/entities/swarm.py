import uuid
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from dataclasses import replace
from uuid import UUID

from .base import Entity


@dataclass(frozen=True, slots=True)
class SwarmEntity(Entity):
    health: str
    queen_year: int
    public_id: UUID = field(default_factory=uuid.uuid4)

    def update(self, public_id: str = "", **kwargs) -> tuple["SwarmEntity", list[str]]:
        data = {k: v for k, v in kwargs.items() if v is not None}
        new_swarm = replace(self, **data)

        updated_fields = [
            field.name for field in fields(new_swarm) if getattr(self, field.name) != getattr(new_swarm, field.name)
        ]

        return new_swarm, updated_fields
