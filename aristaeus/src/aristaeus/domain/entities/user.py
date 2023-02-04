from dataclasses import dataclass
from uuid import UUID

from .base import Entity


@dataclass(frozen=True, slots=True)
class UserEntity(Entity):
    public_id: UUID
    organization_id: UUID
