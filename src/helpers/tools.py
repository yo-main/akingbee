import functools
import datetime

import flask
from peewee import DoesNotExist

from src.helpers.users import get_user_id
from src import constants
from src.constants import trad_codes as trads
from src.constants import alert_codes as alerts
from src.services.alerts import Error
from src.models.comment import Comment
from src.models.swarm import Swarm


def redirect(url):
    return flask.redirect(url)


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
        return f(*args, **kwargs)

    return decorated_function


def get_traductions(index=None):
    language = flask.session["language"]
    return _get_trads(language, index)


def _get_trads(language, index):
    if index is None:
        out = {key: item[language] for key, item in trads.traductions.items()}
    elif index in trads.traductions:
        out = trads.traductions[index][language]
    else:
        raise Error(alerts.TRANSLATION_ID_DOES_NOT_EXISTS)

    return out


def render(url, **kwargs):
    if "language" not in flask.session:
        flask.session["language"] = constants.FRENCH

    return flask.render_template(
        url, lang=flask.session["language"], trads=get_traductions(), **kwargs
    )


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


def update_hive_history(hive):
    try:
        most_recent_comment = (
            Comment.select(Comment)
            .where(Comment.swarm == hive.swarm)
            .order_by(Comment.date.desc(), Comment.id.desc())
            .get()
        )
    except DoesNotExist:
        return True

    if (
        hive.swarm is not None
        and hive.swarm.health != most_recent_comment.health
    ):
        swarm = hive.swarm
        swarm.health = most_recent_comment.health
        swarm.save()

    if (
        most_recent_comment.condition is not None
        and hive.condition != most_recent_comment.condition
    ):
        hive.condition = most_recent_comment.condition
        hive.save()

    return True

def create_system_comment_from_hive(msg, hive):
    comment = Comment(
        comment=msg,
        date=datetime.datetime.now(),
        user=hive.user_id,
        hive=hive.id,
        swarm=hive.swarm_id,
        type=constants.COMMENT_TYPE_SYSTEM,
        apiary=hive.apiary_id,
        condition=hive.condition,
    )

    if hive.swarm:
        comment.health = hive.swarm.health_id

    return comment
