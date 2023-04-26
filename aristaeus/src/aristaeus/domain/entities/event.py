import uuid
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from uuid import UUID

from .base import Entity


@dataclass(slots=True)
class EventEntity(Entity):
    hive_id: UUID
    title: str
    description: str
    due_date: datetime
    type: str
    status: str
    public_id: UUID = field(default_factory=uuid.uuid4)

    def change_title(self, new_title: str):
        self.title = new_title

    def change_description(self, new_description: str):
        self.description = new_description

    def change_due_date(self, new_date: datetime):
        self.due_date = new_date

    def new_status(self, new_status: str):
        self.status = new_status

    def __repr__(self):
        return f"<Event {self.public_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, EventEntity):
            raise ValueError(f"{other} is not a EventEntity")
        return self.public_id == other.public_id

    def __hash__(self) -> int:
        return hash(self.public_id)
