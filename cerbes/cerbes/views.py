import base64
from collections import namedtuple
import datetime
import hashlib
from sqlalchemy.orm import joinedload, Session
import re

from fastapi import APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel
import jwt

from meltingpot.models import Users, Credentials, Owners
from meltingpot.log import logger
from meltingpot.config import CONFIG
from meltingpot.webapp.utils import get_session

from cerbes.helpers import get_password_hash, parse_base_authorization_header, generate_jwt, validate_jwt


router = APIRouter()


class UserModel(BaseModel):
    username: str
    password: str
    email: str



@router.post("/user", status_code=204)
def create_user(user_data: UserModel, session: Session = Depends(get_session)):
    user = Users(email=user_data.email)
    credentials = Credentials(user=user, username=user_data.username, password=get_password_hash(user_data.password))
    owner = Owners(user=user, surname=user_data.username)

    try:
        session.add_all((user, credentials, owner))
        session.commit()
    except Exception:
        logger.exception(f"Could not create user {user_data.email}")
        raise HTTPException(400, "Registration failed")


@router.post("/login", status_code=200)
def authenticate_user(authorization: str = Header(None), session: Session = Depends(get_session)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    credentials = parse_base_authorization_header(authorization)
    if credentials is None:
        raise HTTPException(status_code=401, detail="Could not parse authorization header")

    user_credentials = session.query(Credentials).filter(Credentials.username == credentials.username).one_or_none()
    if user_credentials is None:
        raise HTTPException(status_code=401, detail="Wrong credentials")

    if credentials.password != user_credentials.password:
        raise HTTPException(status_code=401, detail="Wrong credentials")

    user_id = str(user_credentials.user_id)
    return {"access_right": generate_jwt(user_id)}


@router.get("/check", status_code=204)
def check_jwt(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401)

    rgx = re.search("Bearer (.*)$", authorization)
    if rgx is None or len(rgx.groups()) > 1:
        raise HTTPException(status_code=401)

    token = rgx.group(1)
    if not validate_jwt(token):
        raise HTTPException(status_code=401)

