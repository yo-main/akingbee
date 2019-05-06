import sys
import sqlite3
import datetime
import functools

import flask

from app import app
from src.constants import config
from src.constants import trad_codes as trads
from src.constants import alert_codes as alerts
from src.services.error import Error


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
        if flask.session.get('userId') is None:
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


def convertToDate(arg):
    language = flask.session['language']

    if arg == "":
        return ""

    args = list(map(int, arg.split("/")))

    if language == 'fr':
        day = args[0]
        month = args[1]
        year = args[2]
    else:
        day = args[1]
        month = args[0]
        year = args[2]

    myDate = datetime.date(year, month, day)

    return myDate.isoformat()


def updateHealth(bh_id):

    maxHealth = SQL("SELECT MAX(date), health FROM comments WHERE beehouse=?", (bh_id,))
    bhHealth = SQL("SELECT health FROM beehouse WHERE id=?", (bh_id,))

    if maxHealth[0][1] != None and bhHealth[0][0] != maxHealth[0][1]:
        SQL("UPDATE beehouse SET health=? WHERE id=?", (maxHealth[0][1], bh_id))

def getError(arg):
    toReturn = {'result': 'error',
                'code': arg,
                'msg': config.errorMsg[arg]}

    return toReturn

def getSuccess(arg):
    toReturn = {'result': 'success',
                'code': arg,
                'msg': config.successMsg[arg]}

    return toReturn

