import functools

import flask

from src.helpers.users import get_user_id
from src.constants import config
from src.constants import trad_codes as trads
from src.constants import alert_codes as alerts
from src.services.alerts import Error



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


def traductions(index=None):
    language = flask.session["language"]

    if index is None:
        out = {key: item[language] for key, item in trads.traductions.items()}
    elif index in trads.traductions:
        out = {index: trads.traductions[index][language]}
    else:
        raise Error(alerts.TRANSLATION_ID_DOES_NOT_EXISTS)

    return out


def render(url, **kwargs):
    if "language" not in flask.session:
        flask.session["language"] = config.FRENCH

    return flask.render_template(
        url,
        lang=flask.session["language"],
        trads=traductions(),
        **kwargs,
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