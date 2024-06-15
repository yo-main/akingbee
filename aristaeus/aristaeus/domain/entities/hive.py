import uuid
from dataclasses import dataclass
from dataclasses import field
from datetime import date
from uuid import UUID

from aristaeus.domain.errors import ApiaryCannotBeRemovedSwarmExists
from aristaeus.domain.errors import CantAttachSwarmNoApiary
from aristaeus.domain.errors import CantAttachSwarmOneAlreadyExists
from aristaeus.domain.errors import CantHarvestIfNoApiary
from aristaeus.domain.errors import CantHarvestIfNoSwarm
from aristaeus.domain.errors import PermissionError

from .apiary import Apiary
from .base import Entity
from .harvest import Harvest
from .swarm import Swarm


@dataclass
class Hive(Entity):
    name: str
    condition: str
    owner: str
    organization_id: UUID
    public_id: UUID = field(default_factory=uuid.uuid4)
    apiary: Apiary | None = None
    swarm: Swarm | None = None
    harvests: list[Harvest] = field(default_factory=list)

    def transfer_ownership(self, new_owner: str):
        self.owner = new_owner

    def update_condition(self, new_condition: str):
        self.condition = new_condition

    def rename(self, new_name: str):
        self.name = new_name

    def attach_swarm(self, swarm: Swarm):
        if self.apiary is None:
            raise CantAttachSwarmNoApiary(f"Cannot attach swarm to {self} as there's no apiary")

        if self.swarm and self.swarm.public_id != swarm.public_id:
            raise CantAttachSwarmOneAlreadyExists(f"{self} is already attached to {self.swarm}")

        self.swarm = swarm

    def move(self, new_apiary: Apiary):
        if new_apiary.organization_id != self.organization_id:
            raise PermissionError("Permission error")

        self.apiary = new_apiary

    def remove_apiary(self):
        if not self.apiary:
            return

        if self.swarm:
            raise ApiaryCannotBeRemovedSwarmExists(f"Can't remove apiary from {self} when a swarm exists: {self.swarm}")

        self.apiary = None

    def harvest(self, quantity_in_grams: int, date_harvest: date) -> Harvest:
        if not self.apiary:
            raise CantHarvestIfNoApiary(f"Can't harvest on {self} as there's no apiary")

        if not self.swarm:
            raise CantHarvestIfNoSwarm(f"Cant't harvest on {self} if there's no swarm")

        harvest = Harvest(
            quantity=quantity_in_grams, apiary_name=self.apiary.name, date_harvest=date_harvest, hive_id=self.public_id
        )
        if harvest in self.harvests:
            return next(i for i in self.harvests if i == harvest)

        self.harvests.append(harvest)
        return harvest

    def __repr__(self):
        return f"<Hive {self.public_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Hive):
            raise ValueError(f"{other} is not a Hive")
        return self.public_id == other.public_id

    def __hash__(self) -> int:
        return hash(self.public_id)
