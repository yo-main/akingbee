from fastapi import HTTPException

from gaea.log import logger
from gaea.models import Apiaries


def create_apiary(data, session):

    apiary = Apiaries(
        name=data["name"],
        location=data["location"],
        status_id=data["status_id"],
        honey_type_id=data["honey_type_id"],
        user_id=data["user_id"]
    )

    session.add(apiary)

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Something went wrong when saving the object")
        raise HTTPException(status_code=400, detail="Database error")

    return apiary