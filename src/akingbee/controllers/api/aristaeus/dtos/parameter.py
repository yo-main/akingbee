from uuid import UUID

from pydantic import BaseModel


class ParameterIn(BaseModel):
    key: str
    value: str


class ParameterOut(BaseModel):
    public_id: UUID
    key: str
    value: str
    organization_id: UUID
