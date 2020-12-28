import datetime
from enum import Enum
from gaea.log import logger
from gaea.models import SwarmHealthStatuses, HiveConditions, HoneyTypes, EventStatuses, Owners, EventTypes
from gaea.webapp.utils import get_session
from fastapi import APIRouter, Depends, Cookie, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List,Optional
import uuid


from aristaeus.helpers.common import validate_uuid
from aristaeus.helpers.authentication import get_logged_in_user
from aristaeus.models import SetupDataType, SetupDataPostModel, SetupDataModel


router = APIRouter()

MAPPING = {
    "swarm_health_status": SwarmHealthStatuses,
    "apiary_honey_type": HoneyTypes,
    "hive_condition": HiveConditions,
    "hive_beekeeper": Owners,
    "event_type": EventTypes,
    "event_status": EventStatuses,
}

@router.get("/setup/{data_type}", status_code=200, response_model=List[SetupDataModel])
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

@router.post("/setup/{data_type}", status_code=200, response_model=SetupDataModel)
async def create_setup_data(
    body: SetupDataPostModel,
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
    body: SetupDataPostModel,
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

    if obj is None:
        raise HTTPException(status_code=404)
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

    if obj is None:
        raise HTTPException(status_code=404)
    if obj.user_id != user_id:
        raise HTTPException(status_code=403)

    try:
        obj.deleted_at = datetime.datetime.utcnow()
        session.commit()
    except Exception as exc:
        logger.exception("Something went wrong when saving the object")
        raise HTTPException(status_code=400, detail="Database error") from exc
