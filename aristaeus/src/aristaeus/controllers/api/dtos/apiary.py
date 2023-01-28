from uuid import UUID

from pydantic import BaseModel


class PostApiaryIn(BaseModel):
    name: str
    location: str
    honey_kind: str


class PutApiaryIn(BaseModel):
    name: str | None
    location: str | None
    honey_kind: str | None


class ApiaryOut(BaseModel):
    public_id: UUID
    name: str
    location: str
    honey_kind: str
    organization_id: UUID


class DetailedApiaryOut(BaseModel):
    public_id: UUID
    name: str
    location: str
    honey_kind: str
    organization_id: UUID
    hive_count: int
