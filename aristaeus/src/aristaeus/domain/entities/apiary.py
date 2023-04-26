import uuid
from dataclasses import dataclass
from dataclasses import field
from uuid import UUID

from .base import Entity


@dataclass(slots=True)
class ApiaryEntity(Entity):
    name: str
    location: str
    honey_kind: str
    organization_id: UUID
    hive_count: int = 0
    public_id: UUID = field(default_factory=uuid.uuid4)

    def change_location(self, new_location: str):
        self.location = new_location

    def change_honey_kind(self, new_honey_kind: str):
        self.honey_kind = new_honey_kind

    def rename(self, new_name: str):
        self.name = new_name

    def __repr__(self):
        return f"<Apiary {self.public_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ApiaryEntity):
            raise ValueError(f"{other} is not a ApiaryEntity")
        return self.public_id == other.public_id

    def __hash__(self) -> int:
        return hash(self.public_id)
