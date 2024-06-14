from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateSwarmCommand:
    health_status: str
    queen_year: int


@dataclass
class PutSwarmCommand:
    swarm_id: UUID
    health_status: str | None
    queen_year: int | None
