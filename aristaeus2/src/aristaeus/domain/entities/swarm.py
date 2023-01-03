import uuid
from dataclasses import dataclass, field
from uuid import UUID

from .base import Entity


@dataclass(frozen=True, slots=True)
class SwarmEntity(Entity):
    health: str
    queen_year: int
    public_id: UUID = field(default_factory=uuid.uuid4)
