from enum import Enum
from gaea.log import logger
from gaea.models import SwarmHealthStatuses, ApiaryStatuses, HiveConditions, HoneyTypes, EventStatuses
from gaea.webapp.utils import get_session
from fastapi import APIRouter, Depends, Cookie, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session


from aristaeus.helpers.common import validate_uuid
from aristaeus.helpers.authentication import get_logged_in_user
from aristaeus.helpers.models import create_apiary


router = APIRouter()

MAPPING = {
    "swarm_health_status": SwarmHealthStatuses,
    "apiary_status": ApiaryStatuses,
    "honey_type": HoneyTypes,
    "hive_condition": HiveConditions,
    "event_status": EventStatuses,
}

class AddNewSetupData(BaseModel):
    data_type: Enum("Data type", MAPPING)
    value: str


@router.post("/setup", status_code=200)
async def create_new_swarmh_health_status(
    data: AddNewSetupData,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Create an Apiary object and return it as json
    """
    user_id = await get_logged_in_user(access_token)
    model = MAPPING[data["data_type"]]

    obj = model(name=data["value"], user_id=user_id)

    session.add(obj)
    try:
        session.commit()
    except Exception as exc:
        logger.exception("Something went wrong when saving the object")
        raise HTTPException(status_code=400, detail="Database error") from exc

    return obj