from uuid import UUID

from pydantic import BaseModel

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


class HiveOut(BaseModel):
    name: str
    condition: str
    public_id: UUID
    organization_id: UUID
    owner: str
    apiary: ApiaryOut | None
    swarm: SwarmOut | None
