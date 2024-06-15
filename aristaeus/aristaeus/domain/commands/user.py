from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateUserCommand:
    public_id: UUID
    organization_id: UUID
    language: str
    username: str
