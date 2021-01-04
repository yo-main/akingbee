"""API endpoints for hive"""
import datetime
from typing import List
import uuid

from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session

from gaea.log import logger
from gaea.models import Hives
from gaea.webapp.utils import get_session

from aristaeus.helpers.common import validate_uuid
from aristaeus.helpers.authentication import get_logged_in_user
from aristaeus.models import HiveModel, HivePostModel, HivePutModel

router = APIRouter()

@router.get("/hive", status_code=200, response_model=List[HiveModel])
async def get_hives(access_token: str = Cookie(None), session: Session = Depends(get_session)):
    """
    Get a list of hives
    """
    user_id = await get_logged_in_user(access_token)
    hives = session.query(Hives).filter(Hives.user_id == user_id, Hives.deleted_at.is_(None)).all()
    return hives


@router.post("/hive", status_code=200, response_model=HiveModel)
async def post_hive(
    data: HivePostModel,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Create an Hive object and return it as json
    """
    user_id = await get_logged_in_user(access_token)

    hive = Hives(
        name=data.name,
        condition_id=data.condition_id,
        owner_id=data.owner_id,
        swarm_id=data.swarm_id,
        apiary_id=data.apiary_id,
        user_id=user_id,
    )

    session.add(hive)

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Database error", hive=hive)
        raise HTTPException(status_code=400, detail="Couldn't save the hive in database") from exc

    return hive


@router.put("/hive/{hive_id}", status_code=204)
async def put_hive(
    data: HivePutModel,
    hive_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Update an Hive object
    """
    user_id = await get_logged_in_user(access_token)

    if all(v is None for v in data.dict().values()):
        raise HTTPException(400, detail="No argument provided")

    hive = session.query(Hives).get(hive_id)

    if hive is None:
        raise HTTPException(status_code=404)

    if hive.user_id != user_id:
        raise HTTPException(status_code=403)

    for key, value in data.dict().items():
        if value is not None:
            setattr(hive, key, value)

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Database error", hive=hive)
        raise HTTPException(status_code=400, detail="Couldn't update the hive in database") from exc


@router.delete("/hive/{hive_id}", status_code=204)
async def delete_hive(
    hive_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Delete hive
    """
    user_id = await get_logged_in_user(access_token)
    hive = session.query(Hives).get(hive_id)

    if hive is None:
        raise HTTPException(status_code=404)
    if hive.user_id != user_id:
        raise HTTPException(status_code=403)

    try:
        hive.deleted_at = datetime.datetime.utcnow()
        session.commit()
    except Exception as exc:
        logger.exception("Something went wrong when deleting the hive", hive=hive)
        raise HTTPException(status_code=400, detail="Database error") from exc

