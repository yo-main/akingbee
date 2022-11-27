from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator


class CommentIn(BaseModel):
    date: datetime
    type: str
    body: str
    hive_id: UUID
    event_id: UUID | None

    @validator("date")
    def make_due_date_naive(cls, value: datetime):
        return value.replace(tzinfo=None)


class CommentOut(BaseModel):
    public_id: UUID
    date: datetime
    type: str
    body: str
    hive_id: UUID
    event_id: UUID | None
