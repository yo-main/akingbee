#! /home/romain/var/env/py3.6/bin/python3.6
# -*- coding: utf-8 -*-

import flask
import flask_session
import sqlite3
import tempfile
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import os
import datetime
import sys

from app import app
from src.constants import config
from src.constants import alert_codes as alerts
from src.data_access import objects
from src.services.error import Error, Success
from src.helpers.helpers import traductions
from src.helpers.helpers import redirect
from src.helpers.helpers import login_required
from src.helpers.helpers import route


from src.data_access.factory import Factory


factory = Factory()


def render(url, **kwargs):
    if 'language' not in flask.session:
        flask.session['language'] = config.FRENCH

    return flask.render_template(url,
                                 lang=flask.session['language'],
                                 data=traductions(),
                                 **kwargs)


def get_user_from_username(username):
    result = factory.get_from_filters(objects.User, {'username': username})
    if not result or len(result) > 1:
        raise Error(alerts.USER_NOT_FOUND_ERROR)
    return result[0][0]


def get_all(class_, recursive=False):
    return factory.get_from_filters(class_,
                                    {'user': flask.session['user_id']},
                                    recursive=recursive)


@route("/", methods=['GET'])
@login_required
def home():
    return render("akingbee/index_akb.html")


@route("/login", methods=['GET', 'POST'])
def login():

    # We remove the user credentials if any in the cookie
    flask.session.pop('user_id', None)
    flask.session.pop('username', None)

    if flask.request.method == 'GET':
        return render("akingbee/login.html")

    username = flask.request.form.get('username')
    password = flask.request.form.get('password')

    user = get_user_from_username(username)

    if not (password and check_password_hash(user.hash, password)):
        raise Error(alerts.INCORRECT_PASSWORD_ERROR)

    # All good ! We can log in the user
    user.date_last_connection = datetime.datetime.now()
    user.save()

    flask.session['user_id'] = user.id
    flask.session['username'] = user.username

    return Success(alerts.LOGIN_SUCCESS)


@route("/logout", methods=['GET'])
def logout():
    flask.session.pop('user_id', None)
    flask.session.pop('username', None)
    return redirect("/")


@route("/language", methods=['POST'])
def updateLanguage():
    """Change the user language"""
    newLanguage = flask.request.form.get('language')
    flask.session['language'] = newLanguage
    return Success()


@route("/register", methods=['GET'])
def register():
    return render("akingbee/register.html")


@route("/registercheck", methods=['POST'])
def registerCheck():
    data = {
        'username': flask.request.form.get('username'),
        'email': flask.request.form.get('email'),
        'pwd': flask.request.form.get('pwd')
    }

    if factory.count(objects.User, {'username': data['username']}):
        raise Error(alerts.USER_ALREADY_EXISTS_ERROR)
    if factory.count(objects.User, {'email': data['email']}):
        raise Error(alerts.EMAIL_ALREADY_EXISTS_ERROR)

    # Creation of the user
    user = objects.User(data)

    user.pwd = generate_password_hash(data['pwd'],
                                      method='pbkdf2:sha256',
                                      salt_length=8)
    user.save()

    # Creation of all the different data linked to the user
    default_objects = (
        (objects.Health, config.DEFAULT_HEALTH),
        (objects.StatusBeehouse, config.DEFAULT_STATUS_BEEHOUSE),
        (objects.StatusApiary, config.DEFAULT_STATUS_APIARY),
        (objects.BeehouseAction, config.DEFAULT_ACTION_BEEHOUSE),
        (objects.HoneyType, config.DEFAULT_HONEY_KIND),
        (objects.Owner, tuple({'name': user.username}))
    )

    for class_, datas in default_objects:
        for data in datas:
            data['user'] = user.id
            class_(data).save()

    return Success(alerts.REGISTER_SUCCESS)


@route("/reset_password", methods=['GET', 'POST'])
def reset_pwd():
    if flask.session.get('user_id') is not None:
        return redirect("/")

    if flask.request.method == 'GET':
        return render("akingbee/reset_pwd.html")

    if flask.request.method == 'POST':
        pwd = flask.request.form.get('pwd')
        username = flask.request.form.get('username')
        hashed_pwd = generate_password_hash(pwd,
                                            method='pbkdf2:sha256',
                                            salt_length=8)

        user = get_user_from_username(username)
        user.pwd = hashed_pwd
        user.save()

        return Success(alerts.PASSWORD_RESET_SUCCESS)


@route("/apiary/index", methods=['GET'])
@login_required
def apiary():
    apiaries = get_all(objects.Apiary, recursive=True)
    apiary_statuses = get_all(objects.StatusApiary)
    honey_types = get_all(objects.HoneyType)
    location_list = list(set(a.location for a in apiaries))

    return render("akingbee/apiary/index.html",
                  apiaries=apiaries,
                  locations=location_list,
                  apiary_statuses=apiary_statuses,
                  honey_types=honey_types)


@route("/apiary/create", methods=['GET', 'POST'])
@login_required
def apiary_create():
    if flask.request.method == 'GET':
        lang = flask.session['language']

        if lang not in ('fr', 'en'):
            return redirect("/")

        honey_type = helpers.SQL(f"SELECT id, {lang} FROM honey_type WHERE user=?", (flask.session['userId'],))
        status_apiary = helpers.SQL(f"SELECT id, {lang} FROM status_apiary WHERE user=?", (flask.session['userId'],))

        return flask.render_template("akingbee/apiary/create.html", lang=lang, data=helpers.tradDb(lang), honey_type=honey_type, status_apiary=status_apiary)

    elif flask.request.method == 'POST':

        name = flask.request.form.get('apiary_name')
        location = flask.request.form.get('apiary_location')
        honey_type = flask.request.form.get('apiary_honey_type')
        status = flask.request.form.get('apiary_status')
        birthday = helpers.convertToDate(flask.request.form.get('apiary_birthday'))

        flag = helpers.SQL("INSERT INTO apiary(name, location, birthday, status, honey_type, user) VALUES(?,?,?,?,?,?)",
                            (name, location, birthday, status, honey_type, flask.session['userId']))

        return redirect("/apiary/index")


@route("/apiary/create/new_honey_type", methods=['POST'])
@login_required
def apiary_create_honey():

    name_fr = flask.request.form.get('name_fr')
    name_en = flask.request.form.get('name_en')

    flag = helpers.SQL("INSERT INTO honey_type(fr, en, user) VALUES(?,?,?)",
                       (name_fr, name_en, flask.session['userId']))

    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(NEW_PARAMETER_SUCCESS)


@route("/apiary/create/new_apiary_status", methods=['POST'])
@login_required
def apiary_status_create():

    name_fr = flask.request.form.get('name_fr')
    name_en = flask.request.form.get('name_en')

    flag = helpers.SQL("INSERT INTO status_apiary(fr, en, user) VALUES(?,?,?)",
                       (name_fr, name_en, flask.session['userId']))

    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(NEW_PARAMETER_SUCCESS)


@route("/beehouse/index", methods=['GET'])
@login_required
def beehouse():
    lang = flask.session['language']

    if lang not in ('fr', 'en'):
        return redirect("/")

    bh_data = helpers.SQL(f"SELECT beehouse.id, beehouse.name, apiary.name, apiary.location, status_beehouse.{lang}, health.{lang}, owner.name\
                            FROM beehouse\
                            JOIN health ON beehouse.health = health.id\
                            JOIN owner ON beehouse.owner = owner.id\
                            JOIN apiary ON beehouse.apiary = apiary.id\
                            JOIN status_beehouse ON beehouse.status = status_beehouse.id\
                            WHERE beehouse.user=?",
                            (flask.session['userId'],))

    health_filter = helpers.SQL(f"SELECT id, {lang} FROM health WHERE user=?",
                                 (flask.session['userId'],))

    status_beehouse = helpers.SQL(f"SELECT id, {lang} FROM status_beehouse WHERE user=?",
                             (flask.session['userId'],))

    actions_beehouse = helpers.SQL(f"SELECT id, {lang} FROM beehouse_actions WHERE user=?",
                             (flask.session['userId'],))

    apiary_filter = helpers.SQL("SELECT id, name, location FROM apiary WHERE user=?",
                             (flask.session['userId'],))

    owner_filter = helpers.SQL("SELECT id, name FROM owner WHERE user=?",
                                 (flask.session['userId'],))

    return flask.render_template("akingbee/beehouse/index.html", lang=lang, data=helpers.tradDb(lang),
                                 bh=bh_data, af=apiary_filter, hf=health_filter, of=owner_filter, sf=status_beehouse, ab=actions_beehouse)


@route("/beehouse/create", methods=['GET', 'POST'])
@login_required
def beehouse_create():
    if flask.request.method == 'GET':

        lang = flask.session['language']
        owners = helpers.SQL("SELECT id, name FROM owner WHERE user=?", (flask.session['userId'],))
        apiaries = helpers.SQL("SELECT id, name, location FROM apiary WHERE user=?", (flask.session['userId'],))

        if lang not in ('fr', 'en'):
            return redirect("/")

        health = helpers.SQL(f"SELECT id, {lang} FROM health WHERE user=?", (flask.session['userId'],))
        status_beehouse = helpers.SQL(f"SELECT id, {lang} FROM status_beehouse WHERE user=?", (flask.session['userId'],))

        return flask.render_template("akingbee/beehouse/create.html", lang=lang, data=helpers.tradDb(lang), owners=owners,
                                     apiaries=apiaries, health=health, status_beehouse=status_beehouse)

    elif flask.request.method == 'POST':
        name = flask.request.form.get('name')
        birthday = helpers.convertToDate(flask.request.form.get('date'))
        status = flask.request.form.get('status')
        apiary = flask.request.form.get('apiary')
        owner = flask.request.form.get('owner')
        health = flask.request.form.get('health')

        flag = helpers.SQL("INSERT INTO beehouse(name, birthday, apiary, status, health, owner, user) VALUES(?,?,?,?,?,?,?)",
                           (name, birthday, apiary, status, health, owner, flask.session['userId']))

        if flag == False:
            raise Error(SQL_PROCESSING_ERROR)

        return Success(NEW_BEEHOUSE_SUCCESS)


@route("/beehouse/create/new_owner", methods=['POST'])
@login_required
def beehouse_create_owner():

    owner = flask.request.form.get('owner')

    flag = helpers.SQL("INSERT INTO owner(name, user) VALUES(?,?)",
                       (owner, flask.session['userId']))

    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(NEW_BEEKEEPER_SUCCESS)


@route("/beehouse/create/new_health", methods=['POST'])
@login_required
def beehouse_create_health():

    name_fr = flask.request.form.get('name_fr')
    name_en = flask.request.form.get('name_en')

    flag = helpers.SQL("INSERT INTO health(fr, en, user) VALUES(?,?,?)",
                       (name_fr, name_en, flask.session['userId']))

    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(NEW_PARAMETER_SUCCESS)


@route("/beehouse/create/new_beehouse_status", methods=['POST'])
@login_required
def beehouse_create_status():

    name_fr = flask.request.form.get('name_fr')
    name_en = flask.request.form.get('name_en')

    flag = helpers.SQL("INSERT INTO status_beehouse(fr, en, user) VALUES(?,?,?)",
                (name_fr, name_en, flask.session['userId']))

    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(NEW_PARAMETER_SUCCESS)


@route("/beehouse/index/get_beehouse_info", methods=['POST'])
@login_required
def beehouse_details():
    bh_id = flask.request.form.get('bh_id')

    data = helpers.SQL("SELECT name, apiary, status, health, owner\
                        FROM beehouse\
                        WHERE id=? AND user=?",
                        (bh_id, flask.session['userId']))

    return flask.jsonify(data)


@route("/beehouse/index/submit_beehouse_info", methods=['POST'])
@login_required
def submit_beehouse_details():
    bh_id = flask.request.form.get('bh_id')
    apiary = flask.request.form.get('apiary')
    beehouse = flask.request.form.get('beehouse')
    owner = flask.request.form.get('owner')
    status = flask.request.form.get('status')
    user_id = flask.session['userId']

    flags = []

    if apiary != None:
        flags.append(helpers.SQL("UPDATE beehouse SET apiary=? WHERE id=? AND user=?", (apiary, bh_id, user_id)))

    if beehouse != None:
        flags.append(helpers.SQL("UPDATE beehouse SET name=? WHERE id=? AND user=?", (beehouse, bh_id, user_id)))

    if owner != None:
        flags.append(helpers.SQL("UPDATE beehouse SET owner=? WHERE id=? AND user=?", (owner, bh_id, user_id)))

    if status != None:
        flags.append(helpers.SQL("UPDATE beehouse SET status=? WHERE id=? AND user=?", (status, bh_id, user_id)))

    if False in flags:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(MODIFICATION_SUCCESS)


@route("/beehouse/index/submit_comment_modal", methods=['POST'])
@login_required
def submit_comment_modal():
    bh_id = flask.request.form.get('bh_id')
    date = helpers.convertToDate(flask.request.form.get('date'))
    comment = flask.request.form.get('comment')
    health = flask.request.form.get('health')
    cType = '1'

    apiaryId = helpers.SQL("SELECT apiary FROM beehouse WHERE id=? AND user=?", (bh_id, flask.session['userId']))

    if apiaryId is False:
        raise Error(SQL_PROCESSING_ERROR)

    flag = helpers.SQL("INSERT INTO comments(date, comment, beehouse, apiary, health, type, user) VALUES(?,?,?,?,?,?,?)",
                (date, comment, bh_id, apiaryId[0][0], health, cType, flask.session['userId']))

    if flag is False:
        raise Error(SQL_PROCESSING_ERROR)

    helpers.updateHealth(bh_id)

    return Success(MODIFICATION_SUCCESS)


@route("/beehouse/index/submit_action_modal", methods=['POST'])
@login_required
def submit_action_modal():
    bh_id = flask.request.form.get('bh_id')
    date = helpers.convertToDate(flask.request.form.get('date'))
    comment = flask.request.form.get('comment')
    action_type = flask.request.form.get('action_type')
    deadline = helpers.convertToDate(flask.request.form.get('deadline'))
    action_status = 1 # 1 is pending

    flag = helpers.SQL("INSERT INTO actions(beehouse, date, deadline, type, comment, status, user) VALUES(?,?,?,?,?,?,?)",
                       (bh_id, date, deadline, action_type, comment, action_status, flask.session['userId']))

    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(ACTION_PLANIFIED_SUCCESS)


@route("/beehouse", methods=['GET'])
@login_required
def beehouse_profil():
    lang = flask.session['language']
    bh_id = flask.request.args.get('bh')

    if lang not in ('fr', 'en'):
        return redirect("/")

    bh_data = helpers.SQL(f"SELECT beehouse.id, beehouse.name, apiary.name, apiary.location, status_beehouse.{lang}, health.{lang}, owner.name\
                          FROM beehouse\
                          JOIN health ON beehouse.health = health.id\
                          JOIN owner ON beehouse.owner = owner.id\
                          JOIN apiary ON beehouse.apiary = apiary.id\
                          JOIN status_beehouse ON beehouse.status = status_beehouse.id\
                          WHERE beehouse.user=? AND beehouse.id=?",
                          (flask.session['userId'], bh_id))

    cm_data = helpers.SQL(f"SELECT comments.id, strftime('%d/%m/%Y', comments.date), comments_type.{lang}, comments.comment, beehouse.name, apiary.name, apiary.location, coalesce(health.{lang}, '')\
                          FROM comments\
                          JOIN beehouse ON comments.beehouse = beehouse.id\
                          LEFT JOIN health ON comments.health = health.id\
                          JOIN apiary ON comments.apiary = apiary.id\
                          JOIN comments_type ON comments.type = comments_type.id\
                          WHERE comments.user=? AND comments.beehouse=?\
                          ORDER BY comments.date DESC",
                          (flask.session['userId'], bh_id))

    ac_data = helpers.SQL(f"SELECT actions.id, strftime('%d/%m/%Y', actions.date), strftime('%d/%m/%Y', actions.deadline), actions.comment, beehouse_actions.{lang}\
                          FROM actions\
                          JOIN beehouse_actions ON actions.type = beehouse_actions.id\
                          WHERE actions.user=? AND actions.beehouse=? AND actions.status=?\
                          ORDER BY actions.date ASC",
                          (flask.session['userId'], bh_id, 1))

    health_filter = helpers.SQL(f"SELECT id, {lang} FROM health WHERE user=?",
                                (flask.session['userId'],))

    type_filter = helpers.SQL(f"SELECT id, {lang} FROM comments_type")
    bh_status_filter = helpers.SQL(f"SELECT id, {lang} FROM status_beehouse WHERE user=?", (flask.session['userId'],))
    actions_beehouse = helpers.SQL(f"SELECT id, {lang} FROM beehouse_actions WHERE user=?", (flask.session['userId'],))

    apiary_filter = helpers.SQL("SELECT id, name, location FROM apiary WHERE user=?", (flask.session['userId'],))
    owner_filter = helpers.SQL("SELECT id, name FROM owner WHERE user=?", (flask.session['userId'],))

    return flask.render_template("akingbee/beehouse/beehouse_details.html", lang=lang, data=helpers.tradDb(lang), bh=bh_data, cm=cm_data, ac=ac_data,
                                  tf=type_filter, af=apiary_filter, hf=health_filter, of=owner_filter, sf=bh_status_filter, ab=actions_beehouse)


@route("/beehouse/select", methods=['POST'])
@login_required
def select_beehouse():
    bh_id = int(flask.request.form.get('bh_id'))
    way = int(flask.request.form.get('way'))

    data = helpers.SQL("SELECT id FROM beehouse WHERE user=?", (flask.session['userId'],))
    bhs = [n[0] for n in data]
    index = bhs.index(bh_id)
    newId = 0

    if way == -1 and index == 0:
        newId = -1
    elif way == 1 and index == (len(bhs) - 1):
        newId = 0
    else:
        newId = index + way

    return flask.jsonify(f"/beehouse?bh={bhs[newId]}")


@route("/beehouse/index/submit_solve_action_modal", methods=['POST'])
@login_required
def solve_action():
    comment = flask.request.form.get('comment')
    action_id = flask.request.form.get('ac_id')
    action_date = helpers.convertToDate(flask.request.form.get('date'))

    bh_data = helpers.SQL("SELECT beehouse.id, beehouse.apiary\
                           FROM actions\
                           JOIN beehouse ON actions.beehouse = beehouse.id\
                           WHERE actions.id=?",
                           (action_id,))

    bh_id, ap_id = bh_data[0]

    flag = helpers.SQL("INSERT INTO comments(date, comment, beehouse, apiary, action, type, user) VALUES(?,?,?,?,?,?,?)",
                       (action_date, comment, bh_id, ap_id, action_id, 3, flask.session['userId']))
    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    flag = helpers.SQL("UPDATE actions SET date_done=?, status=? WHERE id=? AND user=?",
                       (action_date, 2, action_id, flask.session['userId']))
    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(ACTION_SOLVED_SUCCESS)


@route("/beehouse/index/submit_edit_comment_modal", methods=['POST'])
@login_required
def edit_comment():
    comment = flask.request.form.get('comment')
    cm_id = flask.request.form.get('cm_id')
    health = flask.request.form.get('health')
    date = helpers.convertToDate(flask.request.form.get('date'))

    flag = helpers.SQL("UPDATE comments SET comment=?, health=?, date=? WHERE id=? AND user=?",
                       (comment, health, date, cm_id, flask.session['userId']))
    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    bh_id = helpers.SQL("SELECT beehouse FROM comments WHERE id=? AND user=?", (cm_id, flask.session['userId']))
    helpers.updateHealth(bh_id[0][0])

    return Success(MODIFICATION_SUCCESS)


@route("/beehouse/index/delete_comment", methods=['POST'])
@login_required
def del_comment():
    cm_id = flask.request.form.get('cm_id')
    bh_id, ac_id, type_com = helpers.SQL("SELECT beehouse, action, type FROM comments WHERE id=?", (cm_id,))[0]

    if type_com == 3:
        helpers.SQL("UPDATE actions SET status=?, date_done=? WHERE id=?", (1, None, ac_id))

    helpers.SQL("DELETE FROM comments WHERE id=? AND user=?", (cm_id, flask.session['userId']))
    helpers.updateHealth(bh_id)

    return Success(DELETION_SUCCESS)


@route("/setup", methods=['GET'])
@login_required
def setupPage():
    if flask.request.method == 'GET':
        lang = flask.session['language']
        return flask.render_template("akingbee/setup/setup.html", lang=lang, data=helpers.tradDb(lang), t=0, col="")


@route("/setup/update", methods = ['POST'])
@login_required
def submit_data():
    fr = flask.request.form.get('fr')
    en = flask.request.form.get('en')
    dataId = flask.request.form.get('dataId')
    source = flask.request.form.get('source')

    if source == "/setup/beehouse/status":
        flag = helpers.SQL("UPDATE status_beehouse SET fr=?, en=? WHERE id=? AND user=?", (fr, en, dataId, flask.session['userId']))
    elif source == "/setup/beehouse/owner":
        flag = helpers.SQL("UPDATE owner SET name=? WHERE id=? AND user=?", (fr, dataId, flask.session['userId']))
    elif source == "/setup/beehouse/health":
        flag = helpers.SQL("UPDATE health SET fr=?, en=? WHERE id=? AND user=?", (fr, en, dataId, flask.session['userId']))
    elif source == "/setup/beehouse/honey":
        flag = helpers.SQL("UPDATE honey_type SET fr=?, en=? WHERE id=? AND user=?", (fr, en, dataId, flask.session['userId']))
    elif source == "/setup/beehouse/actions":
        flag = helpers.SQL("UPDATE beehouse_actions SET fr=?, en=? WHERE id=? AND user=?", (fr, en, dataId, flask.session['userId']))
    elif source == "/setup/apiary/status":
        flag = helpers.SQL("UPDATE status_apiary SET fr=?, en=? WHERE id=? AND user=?", (fr, en, dataId, flask.session['userId']))

    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(MODIFICATION_SUCCESS)


@route("/setup/delete", methods=['POST'])
@login_required
def delete_data():
    dataId = flask.request.form.get('dataId')
    source = flask.request.form.get('source')

    if source == "/setup/beehouse/status":
        flag = helpers.SQL("DELETE FROM status_beehouse WHERE id=? AND user=?", (dataId, flask.session['userId']))
    elif source == "/setup/beehouse/owner":
        flag = helpers.SQL("DELETE FROM owner WHERE id=? AND user=?", (dataId, flask.session['userId']))
    elif source == "/setup/beehouse/health":
        flag = helpers.SQL("DELETE FROM health WHERE id=? AND user=?", (dataId, flask.session['userId']))
    elif source == "/setup/beehouse/honey":
        flag = helpers.SQL("DELETE FROM honey_type WHERE id=? AND user=?", (dataId, flask.session['userId']))
    elif source == "/setup/beehouse/actions":
        flag = helpers.SQL("DELETE FROM beehouse_actions WHERE id=? AND user=?", (dataId, flask.session['userId']))
    elif source == "/setup/apiary/status":
        flag = helpers.SQL("DELETE FROM status_apiary WHERE id=? AND user=?", (dataId, flask.session['userId']))

    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(DELETION_SUCCESS)


@route("/setup/submit", methods = ['POST'])
@login_required
def submit_new_data():
    fr = flask.request.form.get('fr')
    en = flask.request.form.get('en')
    source = flask.request.form.get('source')

    if source == "/setup/beehouse/status":
        flag = helpers.SQL("INSERT INTO status_beehouse(fr, en, user) VALUES(?,?,?)", (fr, en, flask.session['userId']))
    elif source == "/setup/beehouse/owner":
        flag = helpers.SQL("INSERT INTO owner(name, user) VALUES(?,?)", (fr, flask.session['userId']))
    elif source == "/setup/beehouse/health":
        flag = helpers.SQL("INSERT INTO health(fr, en, user) VALUES(?,?,?)", (fr, en, flask.session['userId']))
    elif source == "/setup/beehouse/honey":
        flag = helpers.SQL("INSERT INTO honey_type(fr, en, user) VALUES(?,?,?)", (fr, en, flask.session['userId']))
    elif source == "/setup/beehouse/actions":
        flag = helpers.SQL("INSERT INTO beehouse_actions(fr, en, user) VALUES(?,?,?)", (fr, en, flask.session['userId']))
    elif source == "/setup/apiary/status":
        flag = helpers.SQL("INSERT INTO status_apiary(fr, en, user) VALUES(?,?,?)", (fr, en, flask.session['userId']))

    if flag == False:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(NEW_PARAMETER_SUCCESS)


@route("/setup/beehouse/status", methods=['GET', 'POST'])
@login_required
def setupStatusBh():
    if flask.request.method == 'GET':
        lang = flask.session['language']
        menu = 0
        id_title = 'status_beehouse'

        tData = helpers.SQL("SELECT id, fr, en FROM status_beehouse WHERE user=?", (flask.session['userId'],))

        if lang == 'fr':
            title = "Status des ruches"
            desc = "Les différents status qui peut être affecté à une ruche"
        else:
            title = "Beehouse status"
            desc = "The different status that can be given to a beehouse"

        return flask.render_template("akingbee/setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=('fr', 'en'), m=menu, t=title, i=id_title, d=desc)


@route("/setup/beehouse/owner", methods=['GET'])
@login_required
def setupOwner():
    lang = flask.session['language']
    menu = 1
    id_title = 'owner'

    tData = helpers.SQL("SELECT id, name FROM owner WHERE user=?", (flask.session['userId'],))

    if lang == 'fr':
        col = ("Nom",)
        title = "Apiculteur"
        desc = "L'apiculteur d'une ruche (juste au cas où vous gérez les ruches d'une autre personne)"
    else:
        col = ("Name",)
        title = "Beekeper"
        desc = "The beekeper of a beehouse (in case you manage beehouse on behalf of other people ?)"

    return flask.render_template("akingbee/setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=col, m=menu, t=title, i=id_title, d=desc)


@route("/setup/beehouse/health", methods=['GET'])
@login_required
def setupHealth():
    lang = flask.session['language']
    menu = 2
    id_title = 'health'

    tData = helpers.SQL("SELECT id, fr, en FROM health WHERE user=?", (flask.session['userId'],))

    if lang == 'fr':
        title = "Status de santé"
        desc = "Les différents status de santés que vous souhaitez affecter à une ruche"
    else:
        title = "Health status"
        desc = "Different health status that you wish to affect to a beehouse"

    return flask.render_template("akingbee/setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=('fr', 'en'), m=menu, t=title, i=id_title, d=desc)


@route("/setup/beehouse/honey", methods=['GET'])
@login_required
def setupHoneyKind():
    lang = flask.session['language']
    menu = 3
    id_title = 'honey_type'

    tData = helpers.SQL("SELECT id, fr, en FROM honey_type WHERE user=?", (flask.session['userId'],))

    if lang == 'fr':
        title = "Type de miel"
        desc = "Les différents types de miel que vous pouvez être amené à récolter"
    else:
        title = "Honey type"
        desc = "The different kind of honey that you are harvesting"

    return flask.render_template("akingbee/setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=('fr', 'en'), m=menu, t=title, i=id_title, d=desc)


@route("/setup/beehouse/actions", methods=['GET'])
@login_required
def setupBh_actions():
    lang = flask.session['language']
    menu = 4
    id_title = 'beehouse_actions'

    tData = helpers.SQL("SELECT id, fr, en FROM beehouse_actions WHERE user=?", (flask.session['userId'],))

    if lang == 'fr':
        title = "Actions relatives aux ruches"
        desc = "Les différentes actions que vous pouvez être amené à faire sur une ruche"
    else:
        title = "Beehouse actions"
        desc = "The différent actions that you may have to do on a beehouse"

    return flask.render_template("akingbee/setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=('fr', 'en'), m=menu, t=title, i=id_title, d=desc)


@route("/setup/apiary/status", methods=['GET'])
@login_required
def setupStatusAp():
    lang = flask.session['language']
    menu = 5
    id_title = 'status_apiary'

    tData = helpers.SQL("SELECT id, fr, en FROM status_apiary WHERE user=?", (flask.session['userId'],))

    if lang == 'fr':
        title = "Status des ruchers"
        desc = "Les différents status que vous pouvez donner à un rucher"
    else:
        title = "Apiary status"
        desc = "The different status that you may have to give to an apiary"

    return flask.render_template("akingbee/setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=('fr', 'en'), m=menu, t=title, i=id_title, d=desc)


@route("/apiary/index/get_apiary_info", methods=['POST'])
@login_required
def apiary_details():
    ap_id = flask.request.form.get('ap_id')

    data = helpers.SQL("SELECT name, location, status, honey_type\
                        FROM apiary\
                        WHERE id=? AND user=?",
                        (ap_id, flask.session['userId']))

    return flask.jsonify(data)


@route("/apiary/index/submit_apiary_info", methods=['POST'])
@login_required
def submit_apiary_details():
    ap_id = flask.request.form.get('ap_id')

    name = flask.request.form.get('name')
    location = flask.request.form.get('location')
    status = flask.request.form.get('status')
    honey = flask.request.form.get('honey')

    user_id = flask.session['userId']

    flags = []

    if name != None:
        flags.append(helpers.SQL("UPDATE apiary SET name=? WHERE id=? AND user=?", (name, ap_id, user_id)))

    if location != None:
        flags.append(helpers.SQL("UPDATE apiary SET location=? WHERE id=? AND user=?", (location, ap_id, user_id)))

    if status != None:
        flags.append(helpers.SQL("UPDATE apiary SET status=? WHERE id=? AND user=?", (status, ap_id, user_id)))

    if honey != None:
        flags.append(helpers.SQL("UPDATE apiary SET honey=? WHERE id=? AND user=?", (honey, ap_id, user_id)))

    if False in flags:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(MODIFICATION_SUCCESS)


@route("/apiary/delete", methods=['POST'])
@login_required
def del_apiary():
    ap_id = flask.request.form.get('ap_id')
    check = helpers.SQL("DELETE FROM apiary WHERE id=? AND user=?", (ap_id, flask.session['userId']))

    if check == False:
        raise Error(SQL_PROCESSING_ERROR)

    return Success(DELETION_SUCCESS)


if __name__ == "__main__":
    app.run()
