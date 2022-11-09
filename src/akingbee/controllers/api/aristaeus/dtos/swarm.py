from uuid import UUID

from pydantic import BaseModel


class SwarmIn(BaseModel):
    queen_year: int
    health: str


class SwarmOut(BaseModel):
    public_id: UUID
    queen_year: int
    health: str
