"""API endpoints for hive"""
import datetime
from typing import List
import uuid

from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session

from gaea.log import logger
from gaea.models import Hives, Apiaries
from gaea.webapp.utils import get_session

from aristaeus.helpers.common import validate_uuid
from gaea.helpers.auth import get_logged_in_user
from aristaeus.models import HiveModel, HivePostModel, HivePutModel

router = APIRouter()


@router.get("/hive", status_code=200, response_model=List[HiveModel])
async def get_hives(
    access_token: str = Cookie(None), session: Session = Depends(get_session)
):
    """
    Get a list of hives
    """
    user_id = await get_logged_in_user(access_token)
    hives = (
        session.query(Hives)
        .filter(Hives.user_id == user_id, Hives.deleted_at.is_(None))
        .all()
    )

    logger.info("Get list of hives successfull", user_id=user_id, nb_hives=len(hives))
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
    logger.info("Post hive received", user_id=user_id, payload=data)

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
        raise HTTPException(
            status_code=400, detail="Couldn't save the hive in database"
        ) from exc

    logger.info("Post hive successfull", user_id=user_id, hive_id=hive.id)
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
    logger.info("Put hive received", user_id=user_id, payload=data, hive_id=hive_id)

    if all(v is None for v in data.dict().values()):
        raise HTTPException(400, detail="No argument provided")

    hive = session.query(Hives).get(hive_id)

    if hive is None or hive.deleted_at or hive.user_id != user_id:
        raise HTTPException(status_code=404)

    for key, value in data.dict().items():
        if value is not None:
            setattr(hive, key, value)

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Database error", hive=hive)
        raise HTTPException(
            status_code=400, detail="Couldn't update the hive in database"
        ) from exc

    logger.info("Put hive successfull", user_id=user_id, hive_id=hive_id)


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
    logger.info("Delete hive received", user_id=user_id, hive_id=hive_id)

    hive = session.query(Hives).get(hive_id)

    if hive is None or hive.deleted_at or hive.user_id != user_id:
        raise HTTPException(status_code=404)

    try:
        now = datetime.datetime.now()
        hive.deleted_at = now
        hive.apiary_id = None
        # TODO: how to manage swarm when hive is being deleted
        # if hive.swarm:
        # hive.swarm.deleted_at = now

        session.commit()
    except Exception as exc:
        logger.exception("Something went wrong when deleting the hive", hive=hive)
        raise HTTPException(status_code=400, detail="Database error") from exc

    logger.info("Delete hive successfull", user_id=user_id, hive_id=hive_id)


@router.get("/hive/{hive_id}", status_code=200, response_model=HiveModel)
async def get_hive(
    hive_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Get a single hive
    """
    user_id = await get_logged_in_user(access_token)
    hive = session.query(Hives).get(hive_id)

    if hive is None or hive.user_id != user_id or hive.deleted_at:
        raise HTTPException(status_code=404)

    logger.info("Get hive successfull", hive_id=hive_id)
    return hive


@router.put("/hive/{hive_id}/move/{apiary_id}", status_code=204)
async def move_hive(
    hive_id: uuid.UUID,
    apiary_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Move hive to a new apiary
    """
    user_id = await get_logged_in_user(access_token)
    logger.info(
        "Move hive received", user_id=user_id, hive_id=hive_id, new_apiary_id=apiary_id
    )

    hive = session.query(Hives).get(hive_id)

    if hive is None or hive.user_id != user_id or hive.deleted_at:
        raise HTTPException(status_code=404, detail="Hive not found")

    apiary = session.query(Apiaries).get(apiary_id)

    if apiary is None or apiary.user_id != user_id or apiary.deleted_at:
        raise HTTPException(status_code=404, detail="Apiary not found")

    try:
        hive.apiary = apiary
        session.commit()
    except Exception as exc:
        logger.exception(
            "Something went wrong while moving a hive to a new apiary",
            hive=hive,
            apiary=apiary,
        )
        raise HTTPException(status_code=400, detail="Database error") from exc

    logger.info(
        "Apiary successfully moved",
        user_id=user_id,
        new_apiary_id=apiary_id,
        hive_id=hive_id,
    )
