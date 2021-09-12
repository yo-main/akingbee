import datetime
from typing import List, Optional
import uuid

from gaea.log import logger
from gaea.models import Apiaries
from gaea.webapp.utils import get_session
from fastapi import APIRouter, Depends, Cookie, HTTPException
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session

from gaea.helpers.auth import get_logged_in_user
from aristaeus.models import ApiaryPostModel, ApiaryPutModel, ApiaryModel

router = APIRouter()


@router.get("/apiary", status_code=200, response_model=List[ApiaryModel])
async def get_apiaries(
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Create an Apiary object and return it as json
    """
    user_id = await get_logged_in_user(access_token)
    apiaries = (
        session.query(Apiaries)
        .filter(Apiaries.user_id == user_id, Apiaries.deleted_at.is_(None))
        .all()
    )

    logger.info(
        "Get list of apiaries sucessfull", user_id=user_id, nb_apiaries=len(apiaries)
    )
    return apiaries


@router.post("/apiary", status_code=200, response_model=ApiaryModel)
async def post_apiary(
    data: ApiaryPostModel,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Create an Apiary object and return it as json
    """
    user_id = await get_logged_in_user(access_token)
    logger.info("Post apiary received", user_id=user_id, payload=data)

    apiary = Apiaries(
        name=data.name,
        location=data.location,
        honey_type_id=data.honey_type,
        user_id=user_id,
    )

    session.add(apiary)

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Database error", apiary=apiary)
        raise HTTPException(
            status_code=400, detail="Couldn't save the apiary in database"
        ) from exc

    logger.info("Post apiary successfull", apiary_id=apiary.id, user_id=user_id)
    return apiary


@router.delete("/apiary/{apiary_id}", status_code=204)
async def delete_apiary(
    apiary_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Delete apiary
    """
    user_id = await get_logged_in_user(access_token)
    logger.info("Delete apiary received", user_id=user_id, apiary_id=apiary_id)

    apiary = session.query(Apiaries).get(apiary_id)

    if apiary is None or apiary.deleted_at or apiary.user_id != user_id:
        raise HTTPException(status_code=404)

    if apiary.nb_hives > 0:
        raise HTTPException(status_code=400, detail="Hives are linked to this apiary")

    try:
        apiary.deleted_at = datetime.datetime.utcnow()
        session.commit()
    except Exception as exc:
        logger.exception("Something went wrong when deleting the apiary", apiary=apiary)
        raise HTTPException(status_code=400, detail="Database error") from exc

    logger.info("Delete apiary successful", apiary_id=apiary_id, user_id=user_id)


@router.put("/apiary/{apiary_id}", status_code=204)
async def update_apiary(
    body: ApiaryPutModel,
    apiary_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Update an Apiary object
    """
    user_id = await get_logged_in_user(access_token)
    logger.info(
        "Put apiary received", user_id=user_id, payload=body, apiary_id=apiary_id
    )

    if all(v is None for v in body.dict().values()):
        raise HTTPException(400, detail="No argument provided")

    apiary = session.query(Apiaries).get(apiary_id)

    if apiary is None or apiary.deleted_at or apiary.user_id != user_id:
        raise HTTPException(status_code=404)

    for key, value in body.dict().items():
        if value is not None:
            setattr(apiary, key, value)

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Something went wrong when updating the apiary", apiary=apiary)
        raise HTTPException(status_code=400, detail="Database error") from exc

    logger.info("Put apiary successfull", apiary_id=apiary_id, user_id=user_id)
