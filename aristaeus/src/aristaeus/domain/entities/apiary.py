import uuid
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from dataclasses import replace
from uuid import UUID

from .base import Entity


@dataclass(frozen=True, slots=True)
class ApiaryEntity(Entity):
    name: str
    location: str
    honey_kind: str
    organization_id: UUID
    public_id: UUID = field(default_factory=uuid.uuid4)

    def update(
        self, organization_id: str | None = None, public_id: str | None = None, **kwargs
    ) -> tuple["ApiaryEntity", list[str]]:
        data = {k: v for k, v in kwargs.items() if v is not None}
        new_apiary = replace(self, **data)

        updated_fields = [
            field.name for field in fields(new_apiary) if getattr(self, field.name) != getattr(new_apiary, field.name)
        ]

        return new_apiary, updated_fields


@dataclass(frozen=True, slots=True)
class DetailedApiaryEntity(Entity):
    name: str
    location: str
    honey_kind: str
    organization_id: UUID
    public_id: UUID
    hive_count: int