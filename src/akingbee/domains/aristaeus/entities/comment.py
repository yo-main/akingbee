import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from uuid import UUID

from akingbee.domains.aristaeus.entities.vo.reference import Reference


@dataclass(frozen=True, slots=True)
class CommentEntity:
    date: datetime
    type: str  # choice
    body: str

    hive_id: UUID
    event_id: UUID | None
    public_id: UUID = field(default_factory=uuid.uuid4)

    def asdict(self) -> dict:
        return asdict(self)
