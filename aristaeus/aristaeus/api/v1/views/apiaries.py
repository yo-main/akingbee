import uuid

from gaea.models import Apiaries
from gaea.webapp.utils import get_session
from fastapi import APIRouter, Depends, Cookie, HTTPException
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session


from aristaeus.helpers.common import validate_uuid
from aristaeus.helpers.authentication import get_logged_in_user
from aristaeus.helpers.models import create_apiary

router = APIRouter()

class ApiaryPostModel(BaseModel):
    name: constr(min_length=1)
    location: constr(min_length=1)
    status: uuid.UUID
    honey_type: uuid.UUID


@router.get("/apiary", status_code=200)
async def get_apiaries(
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Create an Apiary object and return it as json
    """
    user_id = await get_logged_in_user(access_token)
    apiaries = session.query(Apiaries).filter(Apiaries.user_id == user_id, Apiaries.deleted_at.is_(None)).all()
    return apiaries


@router.post("/apiary", status_code=200)
async def post_apiary(
    data: ApiaryPostModel,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Create an Apiary object and return it as json
    """
    user_id = await get_logged_in_user(access_token)

    if not validate_uuid(data.status):
        raise HTTPException(
            status_code=400, detail=f"Invalid uuid for status: '{data.status}'"
        )
    if not validate_uuid(data.honey_type):
        raise HTTPException(
            status_code=400, detail=f"Invalid uuid for honey_type: '{data.honey_type}'"
        )

    data = {
        "name": data.name,
        "location": data.location,
        "status_id": data.status,
        "honey_type_id": data.honey,
        "user_id": user_id,
    }

    apiary = create_apiary(data=data, session=session)

    return apiary
