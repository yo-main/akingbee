import datetime
from enum import Enum
from gaea.log import logger
from gaea.models import SwarmHealthStatuses, ApiaryStatuses, HiveConditions, HoneyTypes, EventStatuses, Owners, EventTypes
from gaea.webapp.utils import get_session
from fastapi import APIRouter, Depends, Cookie, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List,Optional
import uuid


from aristaeus.helpers.common import validate_uuid
from aristaeus.helpers.authentication import get_logged_in_user
from aristaeus.helpers.models import create_apiary


router = APIRouter()

MAPPING = {
    "swarm_health_status": SwarmHealthStatuses,
    "apiary_status": ApiaryStatuses,
    "apiary_honey_type": HoneyTypes,
    "hive_condition": HiveConditions,
    "hive_beekeeper": Owners,
    "event_type": EventTypes,
    "event_status": EventStatuses,
}

data_type_enum = Enum("data_type", {v:v for v in MAPPING})

class SetupDataType(str, Enum):
    swarm_health_status = "swarm_health_status"
    apiary_status = "apiary_status"
    apiary_honey_type = "apiary_honey_type"
    hive_condition = "hive_condition"
    hive_beekeeper = "hive_beekeeper"
    event_type = "event_type"
    event_status = "event_status"

class NewDataPostModel(BaseModel):
    value: str

    class Config:
        orm_mode = True

class DataModel(BaseModel):
    id: uuid.UUID
    name: str
    user_id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True

@router.get("/setup/{data_type}", status_code=200, response_model=List[DataModel])
async def get_setup_data(
    data_type: SetupDataType,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Get a setup object and return it as json
    """
    user_id = await get_logged_in_user(access_token)
    model = MAPPING[data_type]

    objects = session.query(model).filter(model.user_id == user_id, model.deleted_at.is_(None)).all()

    return objects

@router.post("/setup/{data_type}", status_code=200, response_model=DataModel)
async def create_setup_data(
    body: NewDataPostModel,
    data_type: SetupDataType,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Create a setup object and return it as json
    """
    user_id = await get_logged_in_user(access_token)
    model = MAPPING[data_type]

    obj = model(name=body.value, user_id=user_id)

    session.add(obj)
    try:
        session.commit()
    except Exception as exc:
        logger.exception("Something went wrong when saving the object")
        raise HTTPException(status_code=400, detail="Database error") from exc

    session.refresh(obj)
    return obj

@router.put("/setup/{data_type}/{obj_id}", status_code=204)
async def update_setup_data(
    body: NewDataPostModel,
    data_type: SetupDataType,
    obj_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Update a setup object and return it as json
    """
    user_id = await get_logged_in_user(access_token)
    model = MAPPING[data_type]

    obj = session.query(model).get(obj_id)

    if obj.user_id != user_id:
        raise HTTPException(status_code=403)

    try:
        obj.name = body.value
        session.commit()
    except Exception as exc:
        logger.exception("Something went wrong when saving the object")
        raise HTTPException(status_code=400, detail="Database error") from exc

@router.delete("/setup/{data_type}/{obj_id}", status_code=204)
async def delete_setup_data(
    data_type: SetupDataType,
    obj_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Update a setup object and return it as json
    """
    user_id = await get_logged_in_user(access_token)
    model = MAPPING[data_type]

    obj = session.query(model).get(obj_id)

    if obj.user_id != user_id:
        raise HTTPException(status_code=403)

    try:
        obj.deleted_at = datetime.datetime.utcnow()
        session.commit()
    except Exception as exc:
        logger.exception("Something went wrong when saving the object")
        raise HTTPException(status_code=400, detail="Database error") from exc
