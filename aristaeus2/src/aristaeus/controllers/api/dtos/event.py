from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator


class PostEventIn(BaseModel):
    title: str
    description: str
    due_date: datetime
    status: str
    type: str
    hive_id: UUID

    @validator("due_date")
    def make_due_date_naive(cls, value: datetime):
        return value.replace(tzinfo=None)


class PutEventIn(BaseModel):
    title: str | None
    description: str | None
    due_date: datetime | None
    status: str | None

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
