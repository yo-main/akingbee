"""API endpoints for hive"""
from typing import List
import uuid

from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session

from gaea.log import logger
from gaea.models import Swarms
from gaea.webapp.utils import get_session

from aristaeus.helpers.common import validate_uuid
from aristaeus.helpers.authentication import get_logged_in_user
from aristaeus.models import SwarmModel, SwarmPostModel, SwarmPutModel

router = APIRouter()

@router.get("/swarms", status_code=200, response_model=List[SwarmModel])
async def get_swarms(access_token: str = Cookie(None), session: Session = Depends(get_session)):
    """
    Get a list of swarms
    """
    user_id = await get_logged_in_user(access_token)
    swarms = session.query(Swarms).filter(Swarms.user_id == user_id, Swarms.deleted_at.is_(None)).all()
    return swarms

@router.post("/swarm", status_code=200, response_model=SwarmModel)
async def post_swarm(
    data: SwarmPostModel,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Create an Swarm object and return it as json
    """
    user_id = await get_logged_in_user(access_token)

    if not validate_uuid(data.health_status_id):
        raise HTTPException(
            status_code=400, detail=f"Invalid uuid for the swarm health status: '{data.health_status_id}'"
        )

    swarm = Swarms(
        health_status_id=data.health_status_id,
        user_id=user_id,
    )

    session.add(swarm)

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Database error", swarm=swarm)
        raise HTTPException(status_code=400, detail="Couldn't save the swarm in database") from exc

    return swarm


@router.put("/swarm/{swarm_id}", status_code=204)
async def put_swarm(
    data: SwarmPutModel,
    swarm_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Create an Hive object and return it as json
    """
    user_id = await get_logged_in_user(access_token)

    if not validate_uuid(data.health_status_id):
        raise HTTPException(
            status_code=400, detail=f"Invalid uuid for the swarm health status: '{data.health_status_id}'"
        )

    swarm = session.query(Swarms).get(swarm_id)

    try:
        swarm.health_status_id = data.health_status_id
        session.commit()
    except Exception as exc:
        logger.exception("Database error", swarm=swarm)
        raise HTTPException(status_code=400, detail="Couldn't update the swarm in database") from exc