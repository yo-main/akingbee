
import flask
from peewee import DoesNotExist
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from src.models import User
from src.models import HiveCondition, HoneyType, ActionType, StatusApiary, SwarmHealth, Owner

from src.constants import alert_codes as alerts
from src.constants import config
from src.services.alerts import Error
from src.services.logger import logger

from src.database import DB


def get_user_id():
    user_id = flask.session.get("user_id")
    if user_id is None:
        return None
    return user_id


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
        raise Error(alerts.USER_NOT_FOUND_ERROR)
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
            (HiveCondition, config.DEFAULT_HIVE_CONDITION),
            (StatusApiary, config.DEFAULT_STATUS_APIARY),
            (ActionType, config.DEFAULT_ACTION_TYPE),
            (HoneyType, config.DEFAULT_HONEY_KIND),
            (SwarmHealth, config.DEFAULT_SWARM_HEALTH),
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
