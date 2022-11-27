from uuid import UUID

from pydantic import BaseModel


class ApiaryIn(BaseModel):
    name: str
    location: str
    honey_kind: str


class ApiaryOut(BaseModel):
    public_id: UUID
    name: str
    location: str
    honey_kind: str
    organization_id: UUID
