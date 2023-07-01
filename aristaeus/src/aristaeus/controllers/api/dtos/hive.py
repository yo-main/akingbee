from datetime import date
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field

from .apiary import ApiaryOut
from .swarm import SwarmOut


class PostHiveIn(BaseModel):
    name: str
    condition: str
    owner: str
    apiary_id: UUID | None
    swarm_id: UUID | None


class PutHiveIn(BaseModel):
    name: str | None
    condition: str | None
    owner: str | None
    swarm_id: UUID | None


class HarvestInput(BaseModel):
    quantity_in_grams: int
    date_harvest: date


class HarvestOut(BaseModel):
    quantity: int = Field(alias="quantity_in_grams")
    date_harvest: date

    class Config:
        allow_population_by_field_name = True

class HiveOut(BaseModel):
    name: str
    condition: str
    public_id: UUID
    organization_id: UUID
    owner: str
    apiary: ApiaryOut | None
    swarm: SwarmOut | None
    harvests: list[HarvestOut]
