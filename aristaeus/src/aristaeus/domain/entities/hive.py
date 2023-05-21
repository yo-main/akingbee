import uuid
from dataclasses import dataclass
from dataclasses import field
from uuid import UUID

from aristaeus.domain.errors import ApiaryCannotBeRemovedSwarmExists

from .apiary import Apiary
from .base import Entity
from .swarm import Swarm


@dataclass(slots=True)
class Hive(Entity):
    name: str
    condition: str
    owner: str
    organization_id: UUID
    public_id: UUID = field(default_factory=uuid.uuid4)
    apiary: Apiary | None = None
    swarm: Swarm | None = None

    def transfer_ownership(self, new_owner: str):
        self.owner = new_owner

    def update_condition(self, new_condition: str):
        self.condition = new_condition

    def rename(self, new_name: str):
        self.name = new_name

    def attach_swarm(self, swarm: Swarm):
        if self.apiary is None:
            raise ValueError("Cannot attach a swarm to a hive that is not located on an apiary")  # TODO: refacto that

        if self.swarm:
            raise ValueError("A swarm already exists")  # TODO: refacto that

        self.swarm = swarm

    def move(self, new_apiary: Apiary):
        if new_apiary.organization_id != self.organization_id:
            raise ValueError("Permission error")  # TODO: refacto that

        self.apiary = new_apiary

    def remove_apiary(self):
        if not self.apiary:
            return

        if self.swarm:
            raise ApiaryCannotBeRemovedSwarmExists(f"Can't remove apiary from {self} when a swarm exists: {self.swarm}")

        self.apiary = None

    def __repr__(self):
        return f"<Hive {self.public_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Hive):
            raise ValueError(f"{other} is not a Hive")
        return self.public_id == other.public_id

    def __hash__(self) -> int:
        return hash(self.public_id)
