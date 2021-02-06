import base64
from collections import namedtuple
import datetime
from enum import Enum
import hashlib
from sqlalchemy import exists
from sqlalchemy.orm import joinedload, Session
import re

from fastapi import APIRouter, HTTPException, Depends, Cookie, Header
from pydantic import BaseModel
import jwt

from gaea.models import Users, Credentials, Owners
from gaea.log import logger
from gaea.config import CONFIG
from gaea.webapp.utils import get_session

from cerbes import helpers


router = APIRouter()


class UserModel(BaseModel):
    email: str
    username: str
    password: str


@router.post("/user", status_code=204)
def create_user(
    user_data: UserModel,
    session: Session = Depends(get_session),
    language: str = Cookie(None),
):
    # validate data
    if language not in ("fr", "en"):
        language = "fr"
    if not helpers.validate_email(user_data.email):
        raise HTTPException(400, "Invalid email address")
    if not helpers.validate_password(user_data.password):
        raise HTTPException(400, "Invalid password")
    if session.query(exists().where(Users.email == user_data.email)).scalar():
        raise HTTPException(400, "Email already exists")
    if session.query(
        exists().where(Credentials.username == user_data.username)
    ).scalar():
        raise HTTPException(400, "Username already exists")

    # create all objects
    user = Users(email=user_data.email)
    credentials = Credentials(
        user=user,
        username=user_data.username,
        password=helpers.get_password_hash(user_data.password),
    )
    owner = Owners(user=user, name=user_data.username)

    try:
        session.add_all((user, credentials, owner))
        session.commit()
    except Exception as exc:
        logger.exception(f"Could not create user {user_data.email}")
        raise HTTPException(400, "Database error when creating the user") from exc

    try:
        helpers.send_event_user_created(user_id=user.id, language=language)
    except:  # pylint: disable=bare-except
        logger.exception(
            "Could not insert message about user creation", user_id=user.id
        )


@router.post("/login", status_code=200)
def authenticate_user(
    authorization: str = Header(None), session: Session = Depends(get_session)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    credentials = helpers.parse_authorization_header(authorization)
    if credentials is None:
        raise HTTPException(status_code=401, detail="Could not parse access_token")

    user_credentials = (
        session.query(Credentials)
        .filter(Credentials.username == credentials.username)
        .one_or_none()
    )
    if user_credentials is None or user_credentials.password != credentials.password:
        raise HTTPException(status_code=401, detail="Wrong credentials")

    user_id = str(user_credentials.user_id)
    return {"access_token": helpers.generate_jwt(user_id)}


@router.get("/check", status_code=200)
def check_jwt(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401)

    data = helpers.validate_jwt(access_token)
    if data is None:
        raise HTTPException(status_code=401)

    return {"user_id": data["user_id"]}
