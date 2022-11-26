from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateHiveCommand:
    name: str
    condition: str
    apiary_id: UUID | None
    owner_id: UUID
    organization_id: UUID
