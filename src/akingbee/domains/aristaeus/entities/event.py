import uuid
from dataclasses import dataclass, field
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
