import base64
from collections import namedtuple
import re

from fastapi import APIRouter, Header, HTTPException


CREDENTIALS = namedtuple("credentials", "username, password")
router = APIRouter()


@router.post("/login")
def authenticate_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401)

    credentials = parse_authorization_header(authorization)
    if credentials is None:
        raise HTTPException(status_code=401)


def verify_credentials(credentials):


def parse_authorization_header(authorization):
    rgx = re.search(r"Base (.*)$", authorization)
    if rgx is None:
        return
    token = rgx.group(1)

    try:
        username, password = base64.b64decode(token).decode().split(":")
    except Exception: # pylint: disable=broad-except
        return

    return CREDENTIALS(username, password)


