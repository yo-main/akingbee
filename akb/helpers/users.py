import flask
from peewee import DoesNotExist
from werkzeug.security import check_password_hash, generate_password_hash

from common.log.logger import logger
from common.database import DB
from common.models import User
from common.models import (
    HiveCondition,
    HoneyType,
    EventType,
    StatusApiary,
    SwarmHealth,
    Owner,
)

from akb import constants
from akb.errors import errors


def create_password_hash(password):
    return generate_password_hash(
        password, method="pbkdf2:sha256", salt_length=8
    )


def verify_password(hashed, not_hashed):
    if not not_hashed:
        return False

    if not check_password_hash(hashed, not_hashed):
        return False

    return True


def get_user_from_username(username):
    try:
        result = User.get(User.username == username)
    except DoesNotExist:
        logger.exception(f"Login failed - unknown user: {username}")
        raise errors.UserNotFound(log=False)
    return result


def create_new_user(data):
    with DB.atomic():
        # Creation of the user
        user = User()
        user.username = data["username"]
        user.email = data["email"]
        user.pwd = create_password_hash(data["pwd"])
        user.save()

        # Creation of all the different data linked to the user
        mapping = (
            (HiveCondition, constants.DEFAULT_HIVE_CONDITION),
            (StatusApiary, constants.DEFAULT_STATUS_APIARY),
            (EventType, constants.DEFAULT_EVENT_TYPE),
            (HoneyType, constants.DEFAULT_HONEY_KIND),
            (SwarmHealth, constants.DEFAULT_SWARM_HEALTH),
            (Owner, ({"name": user.username},)),
        )

        for class_, datas in mapping:
            for d in datas:
                try:
                    d["user_id"] = user.id
                    tmp = class_(**d)
                    tmp.save()
                except Exception:
                    logger.critical(
                        "Something bad happened while registering "
                        "a new user with {} and data {}".format(
                            class_.__name__, d
                        )
                    )
                    raise
    return True
