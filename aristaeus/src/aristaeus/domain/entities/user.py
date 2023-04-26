from dataclasses import dataclass
from uuid import UUID

from .base import Entity


@dataclass(frozen=True, slots=True)
class UserEntity(Entity):
    public_id: UUID
    organization_id: UUID

    def __repr__(self):
        return f"<User {self.public_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, UserEntity):
            raise ValueError(f"{other} is not a UserEntity")
        return self.public_id == other.public_id

    def __hash__(self) -> int:
        return hash(self.public_id)
