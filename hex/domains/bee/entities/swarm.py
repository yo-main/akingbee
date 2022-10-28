import uuid
from dataclasses import dataclass, field
from uuid import UUID

from domains.bee.commands.create_swarm import CreateSwarmCommand
from domains.bee.entities.vo.reference import Reference
from domains.bee.errors import OwnershipError


@dataclass(slots=True)
class SwarmEntity:
    health: str
    queen_year: int
    public_id: Reference

    @staticmethod
    def create(health: str, queen_year: int) -> "SwarmEntity":
        return SwarmEntity(
            public_id=Reference.of(uuid.uuid4()),
            queen_year=queen_year,
            health=health,
        )
