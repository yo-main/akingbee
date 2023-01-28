from uuid import UUID
from dataclasses import dataclass


@dataclass
class CreateSwarmCommand:
    health_status: str
    queen_year: int


@dataclass
class PutSwarmCommand:
    swarm_id: UUID
    health_status: str | None
    queen_year: int | None
