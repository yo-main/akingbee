import datetime
from enum import Enum
from pydantic import BaseModel, constr
from typing import Optional
import uuid


class SetupDataType(str, Enum):
    swarm_health_status = "swarm_health_status"
    apiary_honey_type = "apiary_honey_type"
    hive_condition = "hive_condition"
    hive_beekeeper = "hive_beekeeper"
    event_type = "event_type"
    event_status = "event_status"


class SetupDataPostModel(BaseModel):
    value: str


class SetupDataModel(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


# APIARIES


class ApiaryPostModel(BaseModel):
    name: constr(min_length=1)
    location: constr(min_length=1)
    honey_type: uuid.UUID


class ApiaryPutModel(BaseModel):
    name: Optional[constr(min_length=1)]
    location: Optional[constr(min_length=1)]
    honey_type_id: Optional[uuid.UUID]


class ApiaryModel(BaseModel):
    id: uuid.UUID
    name: str
    location: str
    honey_type: SetupDataModel
    nb_hives: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


# SWARMS


class SwarmPostModel(BaseModel):
    health_status_id: uuid.UUID
    queen_year: int


class SwarmPutModel(BaseModel):
    health_status_id: Optional[uuid.UUID] = None
    queen_year: Optional[int] = None


class SwarmModel(BaseModel):
    id: uuid.UUID
    health: SetupDataModel
    queen_year: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


# HIVES


class HivePostModel(BaseModel):
    name: constr(min_length=1)
    condition_id: uuid.UUID
    owner_id: uuid.UUID
    apiary_id: Optional[uuid.UUID] = None
    swarm_id: Optional[uuid.UUID] = None


class HivePutModel(BaseModel):
    name: Optional[constr(min_length=1)] = None
    condition_id: Optional[uuid.UUID] = None
    owner_id: Optional[uuid.UUID] = None
    swarm_id: Optional[uuid.UUID] = None
    apiary_id: Optional[uuid.UUID] = None


class HiveModel(BaseModel):
    id: uuid.UUID
    name: constr(min_length=1)
    condition: SetupDataModel
    owner: SetupDataModel
    swarm: Optional[SwarmModel]
    apiary: Optional[ApiaryModel]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


# EVENTS


class EventStatusModel(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class EventTypeModel(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class EventModel(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    due_date: datetime.datetime
    type: EventTypeModel
    status: EventStatusModel
    hive: Optional[HiveModel]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class PostEventModel(BaseModel):
    title: str
    description: Optional[str]
    due_date: datetime.datetime
    type_id: uuid.UUID
    status_id: uuid.UUID
    hive_id: Optional[uuid.UUID]


class PutEventModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    due_date: Optional[datetime.datetime]
    status_id: Optional[uuid.UUID]


# COMMENTS


class CommentModel(BaseModel):
    id: uuid.UUID
    comment: Optional[str]
    type: str
    date: datetime.datetime
    swarm: Optional[SwarmModel]
    hive: Optional[HiveModel]
    event: Optional[EventModel]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class PostCommentModel(BaseModel):
    comment: str
    date: datetime.datetime
    event_id: Optional[uuid.UUID] = None


class PutCommentModel(BaseModel):
    comment: Optional[str] = None
    date: Optional[datetime.datetime] = None
    event_id: Optional[uuid.UUID] = None
