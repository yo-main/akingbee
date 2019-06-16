import datetime
import functools

import flask

from app import app
from src.constants.environments import URL_ROOT
from src.constants import trad_codes as trads
from src.constants import alert_codes as alerts
from src.services.alerts import Error
from src.data_access.factory import Factory
from src.data_access import objects
from src.constants import environments as ENV


def redirect(url):
    url = URL_ROOT + url
    return flask.redirect(url)


def route(url, **kwargs):
    def my_function(func):
        return app.route(url, **kwargs)(func)

    url = URL_ROOT + url
    return my_function


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if flask.session.get("user_id") is None:
            return redirect("/login")
        else:
            ENV.USER_ID = flask.session.get("user_id")
        return f(*args, **kwargs)

    return decorated_function


def traductions(index=None):
    language = flask.session["language"]

    if index is None:
        out = {key: item[language] for key, item in trads.traductions.items()}
    elif index in trads.traductions:
        out = {index: trads.traductions[index][language]}
    else:
        raise Error(alerts.TRANSLATION_ID_DOES_NOT_EXISTS)

    return out


def update_health(beehouse):
    comments = Factory().get_from_filters(
        objects.Comments, {"beehouse": beehouse.id}
    )
    if comments:
        most_recent_comment = max(comments, key=lambda comment: comment.date)
        beehouse.health = most_recent_comment.health
        beehouse.save()
