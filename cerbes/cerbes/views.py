import base64
from collections import namedtuple
import datetime
from enum import Enum
from typing import List, Optional
import hashlib
import re
from sqlalchemy import exists
from sqlalchemy.orm import joinedload, Session
import uuid

from fastapi import APIRouter, HTTPException, Depends, Cookie, Header
from fastapi.responses import JSONResponse
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


class UserResponseModel(BaseModel):
    id: uuid.UUID
    email: str
    activation_id: Optional[uuid.UUID]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class ListUserResponseModel(BaseModel):
    users: List[UserResponseModel]


class ActivateModel(BaseModel):
    user_id: uuid.UUID
    activation_id: uuid.UUID


class PasswordResetRequestModel(BaseModel):
    username: str


class PasswordResetRequestAnswer(BaseModel):
    reset_id: str


class PasswordResetModel(BaseModel):
    user_id: uuid.UUID
    reset_id: uuid.UUID
    password: str


@router.post("/user", status_code=200, response_model=UserResponseModel)
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
        logger.info(
            f"User created: {user.email}", user_id=user.id, user_email=user.email
        )
    except Exception as exc:
        logger.exception(f"Could not create user {user_data.email}")
        raise HTTPException(400, "Database error when creating the user") from exc

    if not helpers.send_event_user_created(user=user, language=language):
        logger.error(
            "User created but could not publish the rabbitmq message", user_id=user.id
        )

    return user


@router.get("/users", status_code=200, response_model=ListUserResponseModel)
def get_users(
    session: Session = Depends(get_session),
    access_token: str = Cookie(None),
):
    if not access_token:
        raise HTTPException(status_code=401)

    data = helpers.validate_jwt(access_token)
    if data is None:
        raise HTTPException(status_code=401)

    if not (data.get("admin") or data.get("impersonator_id")):
        raise HTTPException(status_code=403)

    users = session.query(Users).filter(Users.deleted_at.is_(None)).all()

    return {"users": users}


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

    user_credentials.last_seen = datetime.datetime.utcnow()
    session.commit()

    logger.info(
        f"User logged in: {credentials.username}",
        user_id=user_id,
        username=user_credentials.username,
    )

    data = {
        "username": user_credentials.username,
        "email": user_credentials.user.email,
        "admin": user_credentials.user.permissions is not None,
    }

    return {"access_token": helpers.generate_jwt(user_id=user_id, extra_data=data)}


@router.get("/refresh", status_code=200)
def refresh_jwt(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401)

    data = helpers.validate_jwt(access_token)
    if data is None:
        raise HTTPException(status_code=401)

    return {
        "access_token": helpers.generate_jwt(user_id=data["user_id"], extra_data=data)
    }


@router.get("/check", status_code=200)
def check_jwt(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401)

    data = helpers.validate_jwt(access_token)
    if data is None:
        raise HTTPException(status_code=401)

    return {"user_id": data["user_id"]}


@router.post("/activate", status_code=201)
def activate_user(
    data: ActivateModel,
    session: Session = Depends(get_session),
):
    user = session.query(Users).get(data.user_id)

    if user is None:
        raise HTTPException(status_code=404)

    if user.activated:
        return JSONResponse(content="Already activated", status_code=200)

    if user.activation_id != data.activation_id:
        raise HTTPException(status_code=400)

    user.activation_id = None
    user.activated = True
    session.commit()

    logger.info(f"User activated: {user.email}", user_id=user.id, user_email=user.email)


@router.post(
    "/password-reset/request",
    status_code=201,
    response_model=PasswordResetRequestAnswer,
)
def reset_user_password_request(
    data: PasswordResetRequestModel,
    session: Session = Depends(get_session),
    language: str = Cookie(None),
):
    user_credentials = (
        session.query(Credentials)
        .join(Users)
        .options(joinedload(Credentials.user))
        .filter(
            (Credentials.username == data.username) | (Users.email == data.username)
        )
        .one_or_none()
    )

    if user_credentials is None:
        raise HTTPException(status_code=404)

    reset_id = uuid.uuid4()
    if not helpers.send_event_user_password_reset(
        user=user_credentials.user, reset_id=reset_id, language=language
    ):
        raise HTTPException(
            status_code=409,
            detail="Password reset requests cannot be handled at the moment",
        )

    user_credentials.reset_id = reset_id
    session.commit()

    logger.info(
        f"User password reset request successful: {user_credentials.user.email}",
        user_id=user_credentials.user.id,
        user_email=user_credentials.user.email,
    )

    return {"reset_id": str(reset_id)}


@router.get("/password-reset/validate", status_code=200)
def validate_reset_id(
    user_id: uuid.UUID, reset_id: uuid.UUID, session: Session = Depends(get_session)
):
    credentials = (
        session.query(Credentials)
        .filter(Credentials.reset_id == reset_id)
        .one_or_none()
    )
    if credentials is None or credentials.user_id != user_id:
        raise HTTPException(status_code=404)


@router.post("/password-reset", status_code=200)
def password_reset(data: PasswordResetModel, session: Session = Depends(get_session)):
    credentials = (
        session.query(Credentials)
        .filter(Credentials.reset_id == data.reset_id)
        .one_or_none()
    )

    if credentials is None or credentials.user_id != data.user_id:
        raise HTTPException(status_code=404)

    if not helpers.validate_password(data.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    credentials.password = helpers.get_password_hash(data.password)
    credentials.reset_id = None
    session.commit()


@router.post("/impersonate/{user_id}", status_code=200)
def impersonate_user(
    user_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    user = session.query(Users).get(user_id)
    if user is None:
        raise HTTPException(status_code=404)

    if not access_token:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    data = helpers.validate_jwt(access_token)
    if data is None:
        raise HTTPException(status_code=401)

    impersonator = (
        session.query(Users).options(joinedload(Users.permissions)).get(data["user_id"])
    )
    if impersonator is None:
        raise HTTPException(status_code=401)

    if impersonator.permissions is None or not impersonator.permissions.impersonate:
        raise HTTPException(status_code=403)

    logger.info(
        f"Impersonating user: {user.email} (by {impersonator.email})",
        user_id=str(user.id),
        impersonator_id=str(impersonator.id),
    )

    data = {
        "username": f"{user.email} ({data['username']})",
        "email": user.email,
        "admin": user.permissions is not None,
        "impersonator_id": str(impersonator.id),
        "impersonator_email": data["email"],
        "impersonator_username": data["username"],
    }

    return {"access_token": helpers.generate_jwt(user_id=user_id, extra_data=data)}


@router.post("/desimpersonate", status_code=200)
def desimpersonate(
    access_token: str = Cookie(None), session: Session = Depends(get_session)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    data = helpers.validate_jwt(access_token)
    if data is None or "impersonator_id" not in data:
        raise HTTPException(status_code=401)

    impersonator = (
        session.query(Users)
        .options(joinedload(Users.permissions))
        .get(data["impersonator_id"])
    )
    if impersonator is None:
        logger.warning("Could not find impersonator. This is odd")
        raise HTTPException(status_code=400)

    logger.info(
        f"Desimpersonating from {impersonator.email}",
        impersonator_id=str(impersonator.id),
    )

    data = {
        "username": data["impersonator_username"],
        "email": data["impersonator_email"],
        "admin": impersonator.permissions is not None,
    }
    return {
        "access_token": helpers.generate_jwt(user_id=impersonator.id, extra_data=data)
    }
