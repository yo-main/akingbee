import base64
from collections import namedtuple
import datetime
import hashlib
import jwt
import re

from meltingpot.config import CONFIG

CREDENTIALS = namedtuple("credentials", "username, password")

def get_password_hash(password):
    sha256 = hashlib.sha256(password.encode())
    return sha256.digest()


def parse_authorization_header(authorization, kind):
    rgx = re.search(f"{kind} (.*)$", authorization)

    if rgx is None:
        return

    token = rgx.group(1)
    print(base64.b64decode(token).decode())

    try:
        username, password = base64.b64decode(token).decode().split(":")
    except Exception: # pylint: disable=broad-except
        return

    return CREDENTIALS(username.strip(), get_password_hash(password.strip()))

def generate_jwt(user_credentials):
    data = {
        "user_id": str(user_credentials.user_id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
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


