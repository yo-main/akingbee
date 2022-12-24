import uuid
from dataclasses import dataclass, field
from uuid import UUID

from .base import Entity


@dataclass(frozen=True, slots=True)
class ParameterEntity(Entity):
    key: str
    value: str
    organization_id: UUID
    public_id: UUID = field(default_factory=uuid.uuid4)

