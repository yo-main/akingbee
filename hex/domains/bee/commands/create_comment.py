from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CreateCommentCommand:
    hive: UUID
    event: UUID | None
    date: datetime
    type: str
    body: str
