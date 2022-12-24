from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator


class EventIn(BaseModel):
    title: str
    description: str
    due_date: datetime
    status: str
    type: str
    hive_id: UUID

    @validator("due_date")
    def make_due_date_naive(cls, value: datetime):
        return value.replace(tzinfo=None)


class EventOut(BaseModel):
    public_id: UUID
    title: str
    description: str
    due_date: datetime
    status: str
    type: str
    hive_id: UUID
