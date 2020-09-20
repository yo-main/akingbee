import base64
from collections import namedtuple
import datetime
import hashlib
import jwt
import re

from gaea.config import CONFIG
from gaea.log import logger

CREDENTIALS = namedtuple("credentials", "username, password")

def validate_email(string):
    """Validate email address. Should cover 99% of cases"""
    pattern = re.compile(r"^[a-z0-9\._%+-]+@[a-z0-9\.-]+\.[a-z]{2,3}$")
    return bool(pattern.match(string))

def validate_password(string):
    """Validate password. Minimum length of 8 and should include at least 1 digit and 1 letter"""
    pattern = re.compile(r"^(?=.*[a-z])(?=.*[0-9]).{8,}$")
    return bool(pattern.match(string))

def get_password_hash(password):
    sha256 = hashlib.sha256(password.encode())
    return sha256.digest()

def parse_authorization_header(auth_header):
    try:
        pattern = re.match(r"Basic (.*)", auth_header)
        creds = pattern.group(1)
        username, password = base64.b64decode(creds).decode().split(":")
    except Exception: # pylint: disable=broad-except
        return

    return CREDENTIALS(username.strip(), get_password_hash(password.strip()))

def generate_jwt(user_id):
    data = {
        "user_id": user_id,
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
            key=CONFIG.APP_SECRET,
            algorithm="HS256"
        )
        return True
    except jwt.exceptions.InvalidTokenError:
        return False


