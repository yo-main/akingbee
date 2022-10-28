from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class OwnerEntity:
    public_id: UUID
    name: str
