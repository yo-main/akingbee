import uuid
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from dataclasses import replace
from datetime import datetime
from uuid import UUID

from .base import Entity


@dataclass(frozen=True, slots=True)
class EventEntity(Entity):
    hive_id: UUID
    title: str
    description: str
    due_date: datetime
    type: str
    status: str
    public_id: UUID = field(default_factory=uuid.uuid4)

    def update(
        self, public_id: str = None, hive_id: str = None, event_id: str = None, **kwargs
    ) -> tuple["EventEntity", list[str]]:
        data = {k: v for k, v in kwargs.items() if v is not None}
        new_event = replace(self, **data)

        updated_fields = [
            field.name for field in fields(new_event) if getattr(self, field.name) != getattr(new_event, field.name)
        ]

        return new_event, updated_fields
