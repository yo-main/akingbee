from dataclasses import dataclass
from datetime import date
from uuid import UUID

from aristaeus.domain.errors import CantHarvestNegativeQuantity

from .base import Entity


@dataclass
class Harvest(Entity):
    quantity: int  # in grams
    apiary_name: str
    hive_id: UUID
    date_harvest: date

    def __post_init__(self):
        if self.quantity < 0:
            raise CantHarvestNegativeQuantity(f"Incorrect quantity to harvest ({self.quantity}) for {self}")

    def __repr__(self):
        return f"<Harvest {self.date_harvest} {self.quantity} grams>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Harvest):
            raise ValueError(f"{other} is not a Harvest")
        return self.date_harvest == other.date_harvest and self.hive_id == other.hive_id

    def __hash__(self) -> int:
        return hash(self.date_harvest)
