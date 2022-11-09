from dataclasses import dataclass


@dataclass
class CreateSwarmCommand:
    health_status: str
    queen_year: int
