from uuid import UUID

from pydantic import BaseModel


class PostHiveIn(BaseModel):
    name: str
    condition: str
    owner_id: UUID
    apiary_id: UUID | None
    swarm_id: UUID | None


class PutHiveIn(BaseModel):
    name: str | None
    condition: str | None
    apiary_id: UUID | None
    swarm_id: UUID | None
    owner_id: UUID | None


class HiveOut(BaseModel):
    name: str
    condition: str
    public_id: UUID
    owner_id: UUID
    organization_id: UUID
    apiary_id: UUID | None
    swarm_id: UUID | None
