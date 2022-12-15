from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateHiveCommand:
    name: str
    condition: str
    apiary_id: UUID | None
    owner_id: UUID
    organization_id: UUID


@dataclass(frozen=True, slots=True)
class PutHiveCommand:
    hive_id: UUID
    name: str | None
    condition: str | None
    apiary_id: UUID | None
    owner_id: UUID | None
