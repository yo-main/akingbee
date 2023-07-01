from dataclasses import dataclass
from dataclasses import field
from datetime import date
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateHiveCommand:
    name: str
    owner: str
    condition: str
    apiary_id: UUID | None
    swarm_id: UUID | None


@dataclass(frozen=True, slots=True)
class PutHiveCommand:
    hive_id: UUID
    name: str | None = field(default=None)
    condition: str | None = field(default=None)
    swarm_id: UUID | None = field(default=None)
    owner: str | None = field(default=None)


@dataclass(frozen=True, slots=True)
class MoveHiveCommand:
    hive_id: UUID
    apiary_id: UUID


@dataclass(frozen=True, slots=True)
class HarvestCommand:
    hive_id: UUID
    quantity_in_grams: int
    date_harvest: date
