import uuid
from dataclasses import asdict, dataclass, field
from uuid import UUID

from .apiary import ApiaryEntity


@dataclass(frozen=True, slots=True)
class HiveEntity:
    name: str
    condition: str
    owner_id: UUID
    organization_id: UUID
    apiary_id: UUID | None
    public_id: UUID = field(default_factory=uuid.uuid4)

    def asdict(self) -> dict:
        return asdict(self)
