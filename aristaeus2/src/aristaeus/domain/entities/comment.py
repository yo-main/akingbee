import uuid
from dataclasses import dataclass, field, fields, replace
from datetime import datetime
from uuid import UUID

from .base import Entity


@dataclass(frozen=True, slots=True)
class CommentEntity(Entity):
    date: datetime
    type: str  # choice
    body: str

    hive_id: UUID
    event_id: UUID | None
    public_id: UUID = field(default_factory=uuid.uuid4)

    def update(
        self, public_id: str = None, hive_id: str = None, event_id: str = None, **kwargs
    ) -> tuple["CommentEntity", list[str]]:
        data = {k: v for k, v in kwargs.items() if v is not None}
        new_comment = replace(self, **data)

        updated_fields = [
            field.name for field in fields(new_comment) if getattr(self, field.name) != getattr(new_comment, field.name)
        ]

        return new_comment, updated_fields
