from dataclasses import dataclass
from dataclasses import field
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateHiveCommand:
    name: str
    owner: str
    condition: str
    apiary_id: UUID | None
    swarm_id: UUID | None
    organization_id: UUID


@dataclass(frozen=True, slots=True)
class PutHiveCommand:
    hive_id: UUID
    name: str | None = field(default=None)
    condition: str | None = field(default=None)
    apiary_id: UUID | None = field(default=None)
    swarm_id: UUID | None = field(default=None)
    owner: str | None = field(default=None)
