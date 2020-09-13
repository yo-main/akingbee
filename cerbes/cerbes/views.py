import base64
from collections import namedtuple
import datetime
import hashlib
from sqlalchemy.orm import joinedload, Session
import re

from fastapi import APIRouter, HTTPException, Depends, Cookie
from pydantic import BaseModel
import jwt

from gaea.models import Users, Credentials, Owners
from gaea.log import logger
from gaea.config import CONFIG
from gaea.webapp.utils import get_session

from cerbes.helpers import get_password_hash, parse_access_token, generate_jwt, validate_jwt


router = APIRouter()


class UserModel(BaseModel):
    email: str
    username: str
    password: str



@router.post("/user", status_code=204)
def create_user(user_data: UserModel, session: Session = Depends(get_session)):
    user = Users(email=user_data.email)
    credentials = Credentials(user=user, username=user_data.username, password=get_password_hash(user_data.password))
    owner = Owners(user=user, surname=user_data.username)

    try:
        session.add_all((user, credentials, owner))
        session.commit()
    except Exception as exc:
        logger.exception(f"Could not create user {user_data.email}")
        raise HTTPException(400, "Database error when creating the user") from exc


@router.post("/login", status_code=200)
def authenticate_user(access_token: str = Cookie(None), session: Session = Depends(get_session)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing access_token")

    credentials = parse_access_token(access_token)
    if credentials is None:
        raise HTTPException(status_code=401, detail="Could not parse access_token")

    user_credentials = session.query(Credentials).filter(Credentials.username == credentials.username).one_or_none()
    if user_credentials is None:
        raise HTTPException(status_code=401, detail="Wrong credentials")

    if credentials.password != user_credentials.password:
        raise HTTPException(status_code=401, detail="Wrong credentials")

    user_id = str(user_credentials.user_id)
    return {"access_right": generate_jwt(user_id)}


@router.get("/check", status_code=204)
def check_jwt(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401)

    if not validate_jwt(access_token):
        raise HTTPException(status_code=401)

