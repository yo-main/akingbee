from dataclasses import asdict, dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserEntity:
    public_id: UUID
    organization_id: UUID

    def asdict(self) -> dict:
        return asdict(self)

    def __eq__(self, other):
        return self.public_id == other.public_id
