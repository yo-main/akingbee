from gaea.models import Apiaries
from gaea.webapp.utils import get_session
from fastapi import APIRouter, Depends, Cookie, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session


from aristaeus.helpers.common import validate_uuid
from aristaeus.helpers.authentication import get_logged_in_user
from aristaeus.helpers.models import create_apiary


router = APIRouter()


class ApiaryPostModel(BaseModel):
    name: str
    location: str
    status: str
    honey_type: str


@router.post("/apiary", status_code=200)
async def create_apiary_request(
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
        "honey_type_id": data.status,
        "user_id": user_id,
    }

    apiary = create_apiary(data=data, session=session)

    return apiary
