from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateEventCommand:
    hive_id: UUID
    due_date: datetime
    type: str
    status: str
    title: str
    description: str


@dataclass(frozen=True, slots=True)
class PutEventCommand:
    event_id: UUID
    due_date: datetime | None
    status: str | None
    title: str | None
    description: str | None
