import uuid
from dataclasses import asdict, dataclass, field
from uuid import UUID

from akingbee.domains.aristaeus.commands.create_swarm import CreateSwarmCommand


@dataclass(frozen=True, slots=True)
class SwarmEntity:
    health: str
    queen_year: int
    public_id: UUID = field(default_factory=uuid.uuid4)

    def asdict(self) -> dict:
        return asdict(self)
