import base64
from collections import namedtuple
import datetime
import hashlib
from sqlalchemy.orm import joinedload, scoped_session
import re

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
import jwt

from meltingpot.models import Users, Credentials, Owners
from meltingpot.database import db
from meltingpot.log import logger
from meltingpot.config import CONFIG

from cerbes.helpers import get_password_hash, parse_authorization_header, generate_jwt, validate_jwt


router = APIRouter()


class UserModel(BaseModel):
    username: str
    password: str
    email: str


@router.post("/user", status_code=204)
def create_user(user_data: UserModel):
    user = Users(email=user_data.email)
    credentials = Credentials(user=user, username=user_data.username, password=get_password_hash(user_data.password))
    owner = Owners(user=user, surname=user_data.username)

    try:
        # pylint: disable=no-member
        db.session.add_all((user, credentials, owner))
        db.session.commit()
    except Exception:
        logger.exception(f"Could not create user {user_data.email}")
        raise HTTPException(400, "Registration failed")


@router.post("/login", status_code=200)
def authenticate_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403, detail="Missing authorization header")

    credentials = parse_authorization_header(authorization, kind="Base")
    if credentials is None:
        raise HTTPException(status_code=403, detail="Could not parse authorization header")

    user_credentials = db.session.query(Credentials).filter(Credentials.username == credentials.username).one_or_none()
    if user_credentials is None:
        raise HTTPException(status_code=403, detail="Wrong credentials")

    if credentials.password != user_credentials.password:
        raise HTTPException(status_code=403, detail="Wrong credentials")

    return generate_jwt(user_credentials)


@router.get("/check", status_code=204)
def check_jwt(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403)

    token = parse_authorization_header(authorization, kind="Bearer")
    if token is None:
        raise HTTPException(status_code=403)

    if not validate_jwt(token):
        raise HTTPException(status_code=403)


