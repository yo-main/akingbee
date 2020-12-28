"""API endpoints for hive"""
from typing import List

from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session

from gaea.log import logger
from gaea.models import Hives
from gaea.webapp.utils import get_session

from aristaeus.helpers.common import validate_uuid
from aristaeus.helpers.authentication import get_logged_in_user
from aristaeus.models import HiveModel, HivePostModel, HivePutModel

router = APIRouter()

@router.get("/hives", status_code=200, response_model=List[HiveModel])
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

    for attr in ("condition_id", "owner_id", "apiary_id"):
        value = getattr(data, attr, None)
        if value is not None and not validate_uuid(value):
            raise HTTPException(
                status_code=400, detail=f"Invalid uuid for {attr}: '{value}'"
            )

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


@router.put("/hive", status_code=204)
async def put_hive(
    data: HivePutModel,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Create an Hive object and return it as json
    """
    user_id = await get_logged_in_user(access_token)

    for attr in ("condition_id", "owner_id", "swarm_id", "apiary_id"):
        if not validate_uuid(getattr(data, attr)):
            raise HTTPException(
                status_code=400, detail=f"Invalid uuid for {attr}: '{getattr(data, attr)}'"
            )

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


