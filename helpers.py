
import functools
import flask
import sqlite3
import datetime
import sys
import akingbee.config

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if flask.session.get('userId') is None:
            return flask.redirect("/akingbee/login")
        return f(*args, **kwargs)
    return decorated_function


def tradDb(language, ind=None):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if language == 'fr':
        if ind == None:
            cursor.execute("SELECT id, fr FROM trad")
        else:
            cursor.execute("SELECT id, fr FROM trad WHERE id=?", ind)
    elif language == 'en':
        if ind == None:
            cursor.execute("SELECT id, en FROM trad")
        else:
            cursor.execute("SELECT id, en FROM trad WHERE id=?", ind)
    
    data = cursor.fetchall()

    toReturn = {}
    for arg in data:
        toReturn[arg[0]] = arg[1]

    conn.close()
    return toReturn


def SQL(request, values =None):
    db = sqlite3.connect("database.db")
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

