from uuid import UUID

from pydantic import BaseModel


class PostSwarmIn(BaseModel):
    queen_year: int
    health: str


class PutSwarmIn(BaseModel):
    queen_year: int | None
    health: str | None


class SwarmOut(BaseModel):
    public_id: UUID
    queen_year: int
    health: str
