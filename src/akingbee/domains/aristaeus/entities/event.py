import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from uuid import UUID

from akingbee.domains.aristaeus.entities.hive import HiveEntity


@dataclass(frozen=True, slots=True)
class EventEntity:
    hive_id: UUID
    title: str
    description: str
    due_date: datetime
    type: str
    status: str
    public_id: UUID = field(default_factory=uuid.uuid4)

    def asdict(self) -> dict:
        return asdict(self)
