import uuid
from dataclasses import dataclass, field
from uuid import UUID

from akingbee.domains.aristaeus.commands.create_swarm import CreateSwarmCommand
from akingbee.domains.aristaeus.entities.vo.reference import Reference


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
