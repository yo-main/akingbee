import uuid
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from uuid import UUID

from .base import Entity


@dataclass(slots=True)
class CommentEntity(Entity):
    date: datetime
    type: str  # choice
    body: str

    hive_id: UUID
    event_id: UUID | None = None
    public_id: UUID = field(default_factory=uuid.uuid4)

    def change_date(self, new_date: datetime):
        self.date = new_date

    def change_body(self, new_body: str):
        self.body = new_body

    def __repr__(self):
        return f"<Comment {self.public_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, CommentEntity):
            raise ValueError(f"{other} is not a CommentEntity")
        return self.public_id == other.public_id

    def __hash__(self) -> int:
        return hash(self.public_id)
