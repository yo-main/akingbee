import uuid
from dataclasses import asdict, dataclass, field
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ApiaryEntity:
    name: str
    location: str
    honey_kind: str
    organization_id: UUID
    public_id: UUID = field(default_factory=uuid.uuid4)

    def asdict(self) -> dict:
        return asdict(self)
