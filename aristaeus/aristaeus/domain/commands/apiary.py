from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateApiaryCommand:
    name: str
    location: str
    honey_kind: str
    organization_id: UUID


@dataclass(frozen=True)
class PutApiaryCommand:
    apiary_id: UUID
    name: str | None
    location: str | None
    honey_kind: str | None
