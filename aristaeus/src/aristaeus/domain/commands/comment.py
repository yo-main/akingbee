from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateCommentCommand:
    hive_id: UUID
    event_id: UUID | None
    date: datetime
    type: str
    body: str


@dataclass(frozen=True, slots=True)
class PutCommentCommand:
    comment_id: UUID
    date: datetime | None
    type: str | None
    body: str | None
