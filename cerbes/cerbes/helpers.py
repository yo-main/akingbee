import base64
import datetime
import hashlib
import re
from collections import namedtuple

import jwt
from gaea.config import CONFIG
from gaea.log import logger
from gaea.rbmq import RBMQPublisher
from gaea.models import Users
from gaea.database import db

CREDENTIALS = namedtuple("credentials", "username, password")


def validate_email(string):
    """Validate email address. Should cover 99% of cases"""
    pattern = re.compile(r"^[a-z0-9\._%+-]+@[a-z0-9\.-]+\.[a-z]{2,4}$")
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
    except Exception:  # pylint: disable=broad-except
        return

    return CREDENTIALS(username.strip(), get_password_hash(password.strip()))


def generate_jwt(user_id, extra_data):
    data = extra_data
    data.update(
        {
            "user_id": str(user_id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            "iss": CONFIG.SERVICE_NAME,
        }
    )

    return jwt.encode(payload=data, key=CONFIG.APP_SECRET, algorithm="HS256")


def validate_jwt(token):
    try:
        return jwt.decode(jwt=token, key=CONFIG.APP_SECRET, algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return None


def send_rbmq_message(routing_key, content):
    rbmq_client = RBMQPublisher()
    try:
        rbmq_client.publish(routing_key=routing_key, content=content)
    except:
        logger.exception(
            "Could not publish rabbitmq message",
            routing_key=routing_key,
            content=content,
        )
        return False
    finally:
        rbmq_client.close()

    return True


def send_event_user_created(user, language):
    content = {
        "user": {
            "id": user.id,
            "email": user.email,
        },
        "language": language,
    }

    if not user.activated:
        activation_link = f"https://{CONFIG.MAIN_HOSTED_ZONE}/activate/{str(user.id)}/{str(user.activation_id)}"
        content["activation_link"] = activation_link

    return send_rbmq_message(routing_key="user.created", content=content)

def send_event_user_password_reset(user, reset_id, language):
    reset_link = f"https://{CONFIG.MAIN_HOSTED_ZONE}/password-reset/{str(user.id)}/{str(reset_id)}"
    content = {
        "user": {
            "id": user.id,
            "email": user.email,
        },
        "language": language,
        "reset_link": reset_link,
    }

    return send_rbmq_message(routing_key="user.reset_password", content=content)


def resync_users():
    session = db().get_session()
    users = session.query(Users).all()
    for user in users:
        send_event_user_created(user, "en")