from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateParameterCommand:
    key: str
    value: str
    organization_id: UUID
