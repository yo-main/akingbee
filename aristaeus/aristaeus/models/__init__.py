import datetime
from enum import Enum
from pydantic import BaseModel, constr
from typing import Optional
import uuid


class SetupDataType(str, Enum):
    swarm_health_status = "swarm_health_status"
    apiary_status = "apiary_status"
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
    status: uuid.UUID
    honey_type: uuid.UUID

class ApiaryPutModel(BaseModel):
    name: Optional[constr(min_length=1)]
    location: Optional[constr(min_length=1)]
    status_id: Optional[uuid.UUID]
    honey_type_id: Optional[uuid.UUID]

class ApiaryModel(BaseModel):
    id: uuid.UUID
    name: str
    location: str
    status: SetupDataModel
    honey_type: SetupDataModel
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


# SWARMS

class SwarmPostModel(BaseModel):
    health_status_id: uuid.UUID

class SwarmModel(BaseModel):
    id: uuid.UUID
    health_status: SetupDataModel
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


# HIVES

class HivePostModel(BaseModel):
    name: constr(min_length=1)
    condition_id: uuid.UUID
    owner_id: uuid.UUID
    swarm_id: uuid.UUID
    apiary_id: uuid.UUID

class HivePutModel(BaseModel):
    name: Optional[constr(min_length=1)]
    condition_id: Optional[uuid.UUID]
    owner_id: Optional[uuid.UUID]
    swarm_id: Optional[uuid.UUID]
    apiary_id: Optional[uuid.UUID]

class HiveModel(BaseModel):
    id: uuid.UUID
    name: constr(min_length=1)
    condition: SetupDataModel
    owner: SetupDataModel
    swarm: SwarmModel
    apiary: ApiaryModel
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
