import uuid
from dataclasses import asdict, dataclass, field, fields, replace
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ApiaryEntity:
    name: str
    location: str
    honey_kind: str
    organization_id: UUID
    public_id: UUID = field(default_factory=uuid.uuid4)

    def asdict(self) -> dict:
        return asdict(self)

    def update(self, organization_id: str = None, public_id: str = None, **kwargs) -> tuple["ApiaryEntity", list[str]]:
        data = {k: v for k, v in kwargs.items() if v is not None}
        new_apiary = replace(self, **data)

        updated_fields = [
            field.name for field in fields(new_apiary) if getattr(self, field.name) != getattr(new_apiary, field.name)
        ]

        return new_apiary, updated_fields
