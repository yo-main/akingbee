from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Languages(str, Enum):
    fr = "fr"
    en = "en"


class User(BaseModel):
    public_id: UUID


class UserCreated(BaseModel):
    language: Languages
    user: User