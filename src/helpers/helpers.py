import datetime
import functools
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import flask

import peewee as pw

from app import app
from src.constants.environments import FLASK_URL_ROOT
from src.constants import trad_codes as trads
from src.constants import alert_codes as alerts
from src.services.alerts import Error

# from src.data_access import objects
# from src.data_access.factory import Factory
from src.data_access.pw_objects import User
from src.data_access.pw_objects import Comment
from src.data_access.pw_objects import Swarm
from src.constants import environments as ENV


def redirect(url):
    url = FLASK_URL_ROOT + url
    return flask.redirect(url)


def route(url, **kwargs):
    def my_function(func):
        return app.route(url, **kwargs)(func)

    url = FLASK_URL_ROOT + url
    return my_function


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_user_id()
        if user_id is None:
            return redirect("/login")
        else:
            ENV.USER_ID = user_id
        return f(*args, **kwargs)

    return decorated_function


def get_user_id():
    user_id = flask.session.get("user_id")
    if user_id is None:
        return None
    return user_id


def create_password_hash(password):
    return generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)


def verify_password(hashed, not_hashed):
    if not not_hashed:
        return False

    if not check_password_hash(hashed, not_hashed):
        return False

    return True


def get_user_from_username(username):
    try:
        result = User.get(User.username == username)
    except pw.DoesNotExist:
        raise Error(alerts.USER_NOT_FOUND_ERROR)
    return result


def traductions(index=None):
    language = flask.session["language"]

    if index is None:
        out = {key: item[language] for key, item in trads.traductions.items()}
    elif index in trads.traductions:
        out = {index: trads.traductions[index][language]}
    else:
        raise Error(alerts.TRANSLATION_ID_DOES_NOT_EXISTS)

    return out


def update_swarm_health(swarm_id):
    if swarm_id is None:
        return False

    comments = list(
        Comment.select().where(Comment.swarm == swarm_id).order_by(Comment.date.desc())
    )

    if comments:
        swarm = Swarm.get_by_id(swarm_id)
        swarm.health = comments[0].health
        swarm.save()

    return True


def get_all(main, *args):
    """
    Fetch a main peewee object with other objects as join
    """
    query = main.select(main, *args)

    for table in args:
        query = query.join(table).switch(main)
    if hasattr(main, "user"):
        query = query.where(main.user == flask.session["user_id"])

    return query
