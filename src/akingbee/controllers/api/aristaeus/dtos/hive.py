from uuid import UUID

from pydantic import BaseModel


class HiveIn(BaseModel):
    name: str
    condition: str
    owner_id: UUID
    organization_id: UUID
    apiary_id: UUID | None


class HiveOut(BaseModel):
    name: str
    condition: str
    public_id: UUID
    owner_id: UUID
    organization_id: UUID
    apiary_id: UUID | None
