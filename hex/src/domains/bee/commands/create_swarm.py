from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateSwarmCommand:
    health_status: str
    queen_year: int
