import uuid
from dataclasses import dataclass
from dataclasses import field
from uuid import UUID

from .apiary import ApiaryEntity
from .base import Entity
from .swarm import SwarmEntity


@dataclass(slots=True)
class HiveEntity(Entity):
    name: str
    condition: str
    owner: str
    organization_id: UUID
    public_id: UUID = field(default_factory=uuid.uuid4)
    apiary: ApiaryEntity | None = None
    swarm: SwarmEntity | None = None

    def transfer_ownership(self, new_owner: str):
        self.owner = new_owner

    def update_condition(self, new_condition: str):
        self.condition = new_condition

    def rename(self, new_name: str):
        self.name = new_name

    def attach_swarm(self, swarm: SwarmEntity):
        if self.swarm:
            raise ValueError("A swarm already exists")  # TODO: refacto that
        self.swarm = swarm

    def move(self, new_apiary: ApiaryEntity):
        if new_apiary.organization_id != self.organization_id:
            raise ValueError("Permission error")  # TODO: refacto that

        self.apiary = new_apiary

    def __repr__(self):
        return f"<Hive {self.public_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, HiveEntity):
            raise ValueError(f"{other} is not a HiveEntity")
        return self.public_id == other.public_id

    def __hash__(self) -> int:
        return hash(self.public_id)
