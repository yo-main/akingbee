from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CreateCommentCommand:
    hive_id: UUID
    event_id: UUID | None
    date: datetime
    type: str
    body: str
