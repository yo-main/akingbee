from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateApiaryCommand:
    name: str
    location: str
    honey_kind: str
    organization_id: UUID


@dataclass
class PutApiaryCommand:
    apiary_id: UUID
    name: str | None
    location: str | None
    honey_kind: str | None
