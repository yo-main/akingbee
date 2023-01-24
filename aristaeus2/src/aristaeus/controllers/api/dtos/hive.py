from uuid import UUID

from pydantic import BaseModel


class PostHiveIn(BaseModel):
    name: str
    condition: str
    owner: str
    apiary_id: UUID | None
    swarm_id: UUID | None


class PutHiveIn(BaseModel):
    name: str | None
    condition: str | None
    owner: str| None
    apiary_id: UUID | None
    swarm_id: UUID | None


class HiveOut(BaseModel):
    name: str
    condition: str
    public_id: UUID
    owner: str
    organization_id: UUID
    apiary_id: UUID | None
    swarm_id: UUID | None
