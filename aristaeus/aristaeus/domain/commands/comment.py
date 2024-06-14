from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateCommentCommand:
    hive_id: UUID
    date: datetime
    type: str
    body: str
    event_id: UUID | None = None


@dataclass(frozen=True, slots=True)
class PutCommentCommand:
    comment_id: UUID
    date: datetime | None
    body: str | None
