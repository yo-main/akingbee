import base64
from collections import namedtuple
import datetime
import hashlib
import re

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
import jwt

from meltingpot.database import Session
from meltingpot.models import Users, Credentials, Owners
from meltingpot.log import logger
from meltingpot.config import CONFIG


CREDENTIALS = namedtuple("credentials", "username, password")
router = APIRouter()


class UserModel(BaseModel):
    username: str
    password: str
    email: str


def get_password_hash(password):
    sha256 = hashlib.sha256(password.encode())
    return sha256.digest()


def parse_authorization_header(authorization, kind):
    rgx = re.search(f"{kind} (.*)$", authorization)

    if rgx is None:
        return

    token = rgx.group(1)

    try:
        username, password = base64.b64decode(token).decode().split(":")
    except Exception: # pylint: disable=broad-except
        return

    return CREDENTIALS(username, get_password_hash(password))

def generate_jwt(user):
    data = {
        "user_id": user.id,
        "exp": datetime.datetime.now + datetime.timedelta(hours=1),
        "iss": CONFIG.SERVICE_NAME
    }

    return jwt.encode(
        payload=data,
        key=CONFIG.APP_SECRET,
        algorithm="HS256"
    )

def validate_jwt(token):
    try:
        jwt.decode(
            jwt=token,
            ket=CONFIG.APP_SECRET,
            algorithm="HS256"
        )
        return True
    except jwt.exceptions.InvalidTokenError:
        return False


@router.post("/user", status_code=204)
def create_user(user_data: UserModel):
    user = Users(email=user_data.email)
    credentials = Credentials(user=user, username=user_data.username, password=get_password_hash(user_data.password))
    owner = Owners(user=user, surname=user_data.username)

    try:
        # pylint: disable=no-member
        Session.add_all((user, credentials, owner))
        Session.commit()
    except Exception:
        logger.exception(f"Could not create user {user_data.email}")
        raise HTTPException(400, "Registration failed")


@router.post("/login", status_code=200)
def authenticate_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403)

    credentials = parse_authorization_header(authorization, kind="Base")
    if credentials is None:
        raise HTTPException(status_code=403)

    user = Session.query.filter(Users.email == credentials.username or Credentials.username == credentials.username).one_or_none()
    if user is None:
        raise HTTPException(status_code=403)

    if user.credentials.password != credentials.password:
        raise HTTPException(status_code=403)

    return generate_jwt(user)


@router.get("/check", status_code=204)
def check_jwt(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403)

    token = parse_authorization_header(authorization, kind="Bearer")
    if token is None:
        raise HTTPException(status_code=403)

    if not validate_jwt(token):
        raise HTTPException(status_code=403)

    return None

