import sys
import sqlite3
import datetime
import functools

import flask

from app import app
from src.constants import config
from src.constants import trad_codes as trads
from src.constants import alert_codes as alerts
from src.services.alerts import Error
from src.data_access.factory import Factory
from src.data_access import objects


def redirect(url):
    url = config.URL_ROOT + url
    return flask.redirect(url)


def route(url, **kwargs):
    def my_function(func):
        return app.route(url, **kwargs)(func)

    url = config.URL_ROOT + url
    return my_function


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if flask.session.get('user_id') is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def traductions(index=None):
    language = flask.session['language']

    if index is None:
        out = {key: item[language] for key, item in trads.traductions.items()}
    elif index in trads.traductions:
        out = {index: trads.traductions[index][language]}
    else:
        raise Error(alerts.TRANSLATION_ID_DOES_NOT_EXISTS)

    return out


def SQL(request, values =None):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    try:
        if values:
            data = cursor.execute(request, values)
        else:
            data = cursor.execute(request)
    except:
        print(request, values)
        print(sys.exc_info())
        db.close()
        return False

    toReturn = data.fetchall()

    db.commit()
    db.close()

    return toReturn


def convert_to_date(arg):
    if arg == "":
        return ""

    args = list(map(int, arg.split("-")))

    day = args[2]
    month = args[1]
    year = args[0]

    myDate = datetime.datetime(year, month, day)

    return myDate


def update_health(beehouse):
    comments = Factory().get_from_filters(objects.Comments,
                                          {'beehouse': beehouse.id})
    if comments:
        most_recent_comment = max(comments, key=lambda comment: comment.date)
        beehouse.health = most_recent_comment.health
        beehouse.save()


def get_error(arg):
    toReturn = {'result': 'error',
                'code': arg,
                'msg': config.errorMsg[arg]}

    return toReturn

def get_success(arg):
    toReturn = {'result': 'success',
                'code': arg,
                'msg': config.successMsg[arg]}

    return toReturn

