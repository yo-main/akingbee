import uuid
from dataclasses import dataclass, field, fields, replace
from uuid import UUID

from .base import Entity

from .apiary import ApiaryEntity
from .swarm import SwarmEntity


@dataclass(frozen=True, slots=True)
class HiveEntity(Entity):
    name: str
    condition: str
    owner: str
    organization_id: UUID
    apiary_id: UUID | None
    swarm_id: UUID | None
    public_id: UUID = field(default_factory=uuid.uuid4)

    def update(self, organization_id: str = "", public_id: str = "", **kwargs) -> tuple["HiveEntity", list[str]]:
        data = {k: v for k, v in kwargs.items() if v is not None}
        new_hive = replace(self, **data)

        updated_fields = [
            field.name for field in fields(new_hive) if getattr(self, field.name) != getattr(new_hive, field.name)
        ]

        return new_hive, updated_fields


@dataclass(frozen=True, slots=True)
class DetailedHiveEntity(Entity):
    name: str
    condition: str
    owner: str
    apiary: ApiaryEntity | None
    swarm: SwarmEntity | None
    public_id: UUID
