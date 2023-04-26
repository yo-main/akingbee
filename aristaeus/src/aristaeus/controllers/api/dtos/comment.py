from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import validator


class PostCommentIn(BaseModel):
    date: datetime
    body: str
    event_id: UUID | None

    @validator("date")
    def make_due_date_naive(cls, value: datetime):
        return value.replace(tzinfo=None)


class PutCommentIn(BaseModel):
    date: datetime | None
    body: str | None

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
