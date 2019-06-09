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

from src.constants import config
from src.constants import alert_codes as alerts
from src.constants.environments import URL_ROOT
from src.data_access import objects
from src.helpers.helpers import traductions
from src.helpers.helpers import redirect
from src.helpers.helpers import login_required
from src.helpers.helpers import route
from src.helpers.helpers import convert_to_date
from src.helpers import helpers
from src.services.alerts import Error, Success
from src.services.logger import logger


from src.data_access.factory import Factory

factory = Factory()


def render(url, **kwargs):
    if 'language' not in flask.session:
        flask.session['language'] = config.FRENCH

    return flask.render_template(url,
                                 lang=flask.session['language'],
                                 trads=traductions(),
                                 url_root=URL_ROOT,
                                 **kwargs)


def get_user_from_username(username):
    result = factory.get_from_filters(objects.User, {'username': username})
    if not result or len(result) > 1:
        raise Error(alerts.USER_NOT_FOUND_ERROR)
    return result[0]


def get_all(class_, deepth=0):
    return factory.get_from_filters(class_,
                                    {'user': flask.session['user_id']},
                                    deepth)


@route("/", methods=['GET'])
@login_required
def home():
    return render("akingbee/index_akb.html")


@route("/login", methods=['GET', 'POST'])
def login():
    logger.info("Connection attempt")

    # We remove the user credentials if any in the cookie
    flask.session['user_id'] = None
    flask.session.pop('username', None)

    if flask.request.method == 'GET':
        return render("akingbee/login.html")

    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    user = get_user_from_username(username)
    if not (password and check_password_hash(user.pwd, password)):
        raise Error(alerts.INCORRECT_PASSWORD_ERROR)

    # All good ! We can log in the user
    user.date_last_connection = datetime.datetime.now()
    user.save()

    flask.session['user_id'] = user.id
    flask.session['username'] = user.username

    return Success(alerts.LOGIN_SUCCESS)


@route("/logout", methods=['GET'])
def logout():
    flask.session['user_id'] = None
    flask.session.pop('username', None)
    return redirect("/")


@route("/language", methods=['POST'])
def updateLanguage():
    """Change the user language"""
    newLanguage = flask.request.form.get('language')

    if newLanguage not in config.LANGUAGES:
        newLanguage = config.ENGLISH

    flask.session['language'] = newLanguage
    return Success()


@route("/register", methods=['GET'])
def register():
    return render("akingbee/register.html")


@route("/registercheck", methods=['POST'])
def registerCheck():
    """
    Will check that we can correctly register a new user
    """
    logger.info("Registration attempt")

    data = {
        'username': flask.request.form.get('username'),
        'email': flask.request.form.get('email'),
        'pwd': flask.request.form.get('pwd')
    }

    if factory.count(objects.User, {'username': data['username']}):
        raise Error(alerts.USER_ALREADY_EXISTS_ERROR)
    if factory.count(objects.User, {'email': data['email']}):
        raise Error(alerts.EMAIL_ALREADY_EXISTS_ERROR)

    facto = Factory(autocommit=False)

    # Creation of the user
    user = objects.User(data)
    user.pwd = generate_password_hash(data['pwd'],
                                      method='pbkdf2:sha256',
                                      salt_length=8)
    user.save(facto)

    # Creation of all the different data linked to the user
    default_objects = (
        (objects.Health, config.DEFAULT_HEALTH),
        (objects.StatusBeehouse, config.DEFAULT_STATUS_BEEHOUSE),
        (objects.StatusApiary, config.DEFAULT_STATUS_APIARY),
        (objects.BeehouseAction, config.DEFAULT_ACTION_BEEHOUSE),
        (objects.HoneyType, config.DEFAULT_HONEY_KIND),
        (objects.Owner, ({'name': user.username},))
    )

    for class_, datas in default_objects:
        for d in datas:
            d['user'] = user.id
            class_(d).save(facto)

    facto.commit()

    return Success(alerts.REGISTER_SUCCESS)


@route("/reset_password", methods=['GET', 'POST'])
def reset_pwd():
    if flask.session['user_id'] is not None:
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
    apiaries = get_all(objects.Apiary, deepth=2)
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
        honey_types = factory.get_all(objects.HoneyType)
        apiary_statuses = factory.get_all(objects.StatusApiary)

        return render("akingbee/apiary/create.html",
                      honey_types=honey_types,
                      apiary_statuses=apiary_statuses)

    elif flask.request.method == 'POST':
        data = {
            'name': flask.request.form.get('name'),
            'location': flask.request.form.get('location'),
            'honey_type': flask.request.form.get('honey_type'),
            'status': flask.request.form.get('status'),
            'birthday': convert_to_date(flask.request.form.get('birthday')),
        }

        apiary = objects.Apiary(data)
        apiary.save()

        return Success(alerts.NEW_APIARY_SUCCESS)


@route("/apiary/create/new_honey_type", methods=['POST'])
@login_required
def apiary_create_honey():
    data = {
        'fr': flask.request.form.get('name_fr'),
        'en': flask.request.form.get('name_en'),
    }

    honey = objects.HoneyType(data)
    honey.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@route("/apiary/create/new_apiary_status", methods=['POST'])
@login_required
def apiary_status_create():
    data = {
        'fr': flask.request.form.get('name_fr'),
        'en': flask.request.form.get('name_en'),
    }

    status_apiary = objects.StatusApiary(data)
    status_apiary.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@route("/beehouse/index", methods=['GET'])
@login_required
def beehouse():
    with Factory() as facto:
        beehouses = facto.get_all(objects.Beehouse, deepth=2)
        healths = facto.get_all(objects.Health)
        beehouse_statuses = facto.get_all(objects.StatusBeehouse)
        beehouse_actions = facto.get_all(objects.BeehouseAction)
        apiaries = facto.get_all(objects.Apiary)
        owners = facto.get_all(objects.Owner)

    return render("akingbee/beehouse/index.html",
                  beehouses=beehouses,
                  apiaries=apiaries,
                  healths=healths,
                  owners=owners,
                  beehouse_statuses=beehouse_statuses,
                  beehouse_actions=beehouse_actions)


@route("/beehouse/create", methods=['GET', 'POST'])
@login_required
def beehouse_create():
    if flask.request.method == 'GET':
        with Factory() as facto:
            owners = facto.get_all(objects.Owner)
            apiaries = facto.get_all(objects.Apiary)
            healths = facto.get_all(objects.Health)
            beehouse_statuses = facto.get_all(objects.StatusBeehouse)

        return render("akingbee/beehouse/create.html",
                      owners=owners,
                      apiaries=apiaries,
                      healths=healths,
                      beehouse_statuses=beehouse_statuses)

    elif flask.request.method == 'POST':
        data = {
            'name': flask.request.form.get('name'),
            'birthday': convert_to_date(flask.request.form.get('date')),
            'status': flask.request.form.get('status'),
            'apiary': flask.request.form.get('apiary'),
            'owner': flask.request.form.get('owner'),
            'health': flask.request.form.get('health'),
        }

        beehouse = objects.Beehouse(data)
        beehouse.save()

        return Success(alerts.NEW_BEEHOUSE_SUCCESS)


@route("/beehouse/create/new_owner", methods=['POST'])
@login_required
def beehouse_create_owner():
    data = {
        'name': flask.request.form.get('owner')
    }
    owner = objects.Owner(data)
    owner.save()

    return Success(alerts.NEW_BEEKEEPER_SUCCESS)


@route("/beehouse/create/new_health", methods=['POST'])
@login_required
def beehouse_create_health():
    data = {
        'fr': flask.request.form.get('name_fr'),
        'en': flask.request.form.get('name_en'),
    }
    health = objects.Health(data)
    health.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@route("/beehouse/create/new_beehouse_status", methods=['POST'])
@login_required
def beehouse_create_status():
    data = {
        'fr': flask.request.form.get('name_fr'),
        'en': flask.request.form.get('name_en'),
    }
    beehouse_status = objects.StatusBeehouse(data)
    beehouse_status.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@route("/beehouse/index/get_beehouse_info", methods=['POST'])
@login_required
def beehouse_details():
    bh_id = flask.request.form.get('bh_id')
    beehouse = factory.get_from_id(bh_id, objects.Beehouse)
    return flask.jsonify(beehouse.serialize())


@route("/beehouse/index/submit_beehouse_info", methods=['POST'])
@login_required
def submit_beehouse_details():
    beehouse = factory.get_from_id(flask.request.form.get('bh_id'),
                                   objects.Beehouse)
    beehouse.apiary = flask.request.form.get('apiary')
    beehouse.name = flask.request.form.get('beehouse')
    beehouse.owner = flask.request.form.get('owner')
    beehouse.status = flask.request.form.get('status')
    beehouse.save()

    return Success(alerts.MODIFICATION_SUCCESS)


@route("/beehouse/index/submit_comment_modal", methods=['POST'])
@login_required
def submit_comment_modal():
    beehouse = factory.get_from_id(flask.request.form.get('bh_id'),
                                   objects.Beehouse)
    comment_data = {
        'beehouse': beehouse.id,
        'apiary': beehouse.apiary,
        'date': convert_to_date(flask.request.form.get('date')),
        'comment': flask.request.form.get('comment'),
        'health': flask.request.form.get('health'),
        'type': config.STATUS_PENDING,
    }
    comment = objects.Comments(comment_data)
    comment.save()

    helpers.update_health(beehouse)

    return Success(alerts.MODIFICATION_SUCCESS)


@route("/beehouse/index/submit_action_modal", methods=['POST'])
@login_required
def submit_action_modal():
    data = {
        'beehouse': flask.request.form.get('bh_id'),
        'date': convert_to_date(flask.request.form.get('date')),
        'comment': flask.request.form.get('comment'),
        'type': flask.request.form.get('action_type'),
        'deadline': convert_to_date(flask.request.form.get('deadline')),
        'status': config.STATUS_PENDING
    }
    action = objects.Actions(data)
    action.save()

    return Success(alerts.ACTION_PLANIFICATION_SUCCESS)


@route("/beehouse", methods=['GET'])
@login_required
def beehouse_profil():
    bh_id = flask.request.args.get('bh')
    facto = Factory(autocommit=False)

    beehouse = facto.get_from_id(bh_id, objects.Beehouse, deepth=1)

    comments = facto.get_from_filters(objects.Comments,
                                      {'beehouse': int(bh_id)},
                                      deepth=2)

    action_filters = {'beehouse': bh_id, 'status': config.STATUS_PENDING}
    actions = facto.get_from_filters(objects.Actions,
                                     action_filters,
                                     deepth=0)
    healths = facto.get_all(objects.Health)
    comment_types = facto.get_all(objects.CommentsType)
    beehouse_statuses = facto.get_all(objects.StatusBeehouse)
    beehouse_actions = facto.get_all(objects.BeehouseAction)
    apiaries = facto.get_all(objects.Apiary)
    owners = facto.get_all(objects.Owner)

    facto.commit()

    return render("akingbee/beehouse/beehouse_details.html",
                  beehouse=beehouse,
                  comments=comments,
                  actions=actions,
                  comment_types=comment_types,
                  apiaries=apiaries,
                  healths=healths,
                  owners=owners,
                  beehouse_statuses=beehouse_statuses,
                  beehouse_actions=beehouse_actions)


@route("/beehouse/select", methods=['POST'])
@login_required
def select_beehouse():
    bh_id = int(flask.request.form.get('bh_id'))
    way = int(flask.request.form.get('way'))

    beehouses = factory.get_all(objects.Beehouse)
    index = beehouses.index(bh_id)

    if way == -1 and index <= 0:
        new_id = beehouses[-1].id
    elif way == 1 and index >= (len(beehouses) - 1):
        new_id = beehouses[0].id
    else:
        new_id = beehouses[index + way].id

    return flask.jsonify(f"/beehouse?bh={new_id}")


@route("/beehouse/index/submit_solve_action_modal", methods=['POST'])
@login_required
def solve_action():

    action = factory.get_from_id(flask.request.form.get('ac_id'),
                                 objects.Actions)
    beehouse = factory.get_from_id(action.beehouse, objects.Beehouse)

    data = {
        'comment': flask.request.form.get('comment'),
        'date': convert_to_date(flask.request.form.get('date')),
        'action': action.id,
        'beehouse': beehouse.id,
        'apiary': beehouse.apiary,
        'type': config.COMMENT_TYPE_ACTION,
    }

    comment = objects.Comments(data)
    comment.save()

    action.date_done = data['date']
    action.status = config.STATUS_DONE
    action.save()

    return Success(alerts.ACTION_SOLVED_SUCCESS)


@route("/beehouse/index/submit_edit_comment_modal", methods=['POST'])
@login_required
def edit_comment():
    comment = factory.get_from_id(flask.request.form.get('cm_id'),
                                  objects.Comments)

    comment.comment = flask.request.form.get('comment')
    comment.health = flask.request.form.get('health')
    comment.date = convert_to_date(flask.request.form.get('date'))
    comment.save()

    beehouse = factory.get_from_id(comment.beehouse, objects.Beehouse)
    helpers.update_health(beehouse)

    return Success(alerts.MODIFICATION_SUCCESS)


@route("/beehouse/index/delete_comment", methods=['POST'])
@login_required
def del_comment():
    comment = factory.get_from_id(flask.request.form.get('cm_id'),
                                  objects.Comments)

    if comment.type == config.COMMENT_TYPE_ACTION:
        action = factory.get_from_id(comment.action, objects.Actions)
        action.status = config.STATUS_PENDING
        action.date_done = None
        action.save()

    comment.delete()

    beehouse = factory.get_from_id(comment.beehouse, objects.Beehouse)
    helpers.update_health(beehouse)

    return Success(alerts.DELETION_SUCCESS)


@route("/setup", methods=['GET'])
@login_required
def setupPage():
    if flask.request.method == 'GET':
        return render("akingbee/setup/setup.html", title=0, columns="")


@route("/setup/update", methods=['POST'])
@login_required
def submit_data():
    fr = flask.request.form.get('fr')
    en = flask.request.form.get('en')
    data_id = flask.request.form.get('dataId')
    source = flask.request.form.get('source')

    if "/setup/beehouse/status" in source:
        obj = factory.get_from_id(data_id, objects.StatusBeehouse)
        obj.fr = fr
        obj.en = en
    elif "/setup/beehouse/owner" in source:
        obj = factory.get_from_id(data_id, objects.Owner)
        obj.name = fr
    elif "/setup/beehouse/health" in source:
        obj = factory.get_from_id(data_id, objects.Health)
        obj.fr = fr
        obj.en = en
    elif "/setup/beehouse/honey" in source:
        obj = factory.get_from_id(data_id, objects.HoneyType)
        obj.fr = fr
        obj.en = en
    elif "/setup/beehouse/actions" in source:
        obj = factory.get_from_id(data_id, objects.BeehouseAction)
        obj.fr = fr
        obj.en = en
    elif "/setup/apiary/status" in source:
        obj = factory.get_from_id(data_id, objects.StatusApiary)
        obj.fr = fr
        obj.en = en
    else:
        raise Error(alerts.INTERNAL_ERROR)

    obj.save()

    return Success(alerts.MODIFICATION_SUCCESS)


@route("/setup/delete", methods=['POST'])
@login_required
def delete_data():
    data_id = flask.request.form.get('dataId')
    source = flask.request.form.get('source')

    if "/setup/beehouse/status" in source:
        obj = factory.get_from_id(data_id, objects.StatusBeehouse)
    elif "/setup/beehouse/owner" in source:
        obj = factory.get_from_id(data_id, objects.Owner)
    elif "/setup/beehouse/health" in source:
        obj = factory.get_from_id(data_id, objects.Health)
    elif "/setup/beehouse/honey" in source:
        obj = factory.get_from_id(data_id, objects.HoneyType)
    elif "/setup/beehouse/actions" in source:
        obj = factory.get_from_id(data_id, objects.BeehouseAction)
    elif "/setup/apiary/status" in source:
        obj = factory.get_from_id(data_id, objects.StatusApiary)
    else:
        raise Error(alerts.INTERNAL_ERROR)

    obj.delete()

    return Success(alerts.DELETION_SUCCESS)


@route("/setup/submit", methods=['POST'])
@login_required
def submit_new_data():
    fr = flask.request.form.get('fr')
    en = flask.request.form.get('en')
    source = flask.request.form.get('source')

    if "/setup/beehouse/status" in source:
        obj = objects.StatusBeehouse({'fr': fr, 'en': en})
    elif "/setup/beehouse/owner" in source:
        obj = objects.Owner({'name': fr})
    elif "/setup/beehouse/health" in source:
        obj = objects.Health({'fr': fr, 'en': en})
    elif "/setup/beehouse/honey" in source:
        obj = objects.HoneyType({'fr': fr, 'en': en})
    elif "/setup/beehouse/actions" in source:
        obj = objects.BeehouseAction({'fr': fr, 'en': en})
    elif "/setup/apiary/status" in source:
        obj = objects.StatusApiary({'fr': fr, 'en': en})
    else:
        raise Error(alerts.INTERNAL_ERROR)

    obj.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@route("/setup/beehouse/status", methods=['GET'])
@login_required
def setupStatusBh():
    lang = flask.session['language']
    menu = 0
    id_title = 'status_beehouse'
    beehouse_statuses = factory.get_all(objects.StatusBeehouse)

    if lang == config.FRENCH:
        title = "Status des ruches"
        description = ("Les différents status qui peuvent "
                       "être affectés à une ruche")
    else:
        title = "Beehouse status"
        description = ("The different status that can "
                       "be given to a beehouse")

    return render("akingbee/setup/setup.html",
                  object_data=beehouse_statuses,
                  columns=(config.FRENCH, config.ENGLISH),
                  menu=menu,
                  title=title,
                  id_title=id_title,
                  description=description)


@route("/setup/beehouse/owner", methods=['GET'])
@login_required
def setupOwner():
    lang = flask.session['language']
    menu = 1
    id_title = 'owner'

    owners = factory.get_all(objects.Owner)

    if lang == config.FRENCH:
        columns = ("Nom",)
        title = "Apiculteur"
        description = ("L'apiculteur d'une ruche (juste au cas "
                       "où vous gérez les ruches d'une autre personne)")
    else:
        columns = ("Name",)
        title = "Beekeper"
        description = ("The beekeper of a beehouse (in case "
                       "you manage beehouse on behalf of other people ?)")

    return render("akingbee/setup/setup.html",
                  object_data=owners,
                  columns=columns,
                  menu=menu,
                  title=title,
                  id_title=id_title,
                  description=description)


@route("/setup/beehouse/health", methods=['GET'])
@login_required
def setupHealth():
    lang = flask.session['language']
    menu = 2
    id_title = 'health'

    healths = factory.get_all(objects.Health)

    if lang == config.FRENCH:
        title = "Status de santé"
        description = ("Les différents status de santés "
                       "que vous souhaitez affecter à une ruche")
    else:
        title = "Health status"
        description = ("Different health status that "
                       "you wish to affect to a beehouse")

    return render("akingbee/setup/setup.html",
                  object_data=healths,
                  columns=('fr', 'en'),
                  menu=menu,
                  title=title,
                  id_title=id_title,
                  description=description)


@route("/setup/beehouse/honey", methods=['GET'])
@login_required
def setupHoneyKind():
    lang = flask.session['language']
    menu = 3
    id_title = 'honey_type'

    honey_types = factory.get_all(objects.HoneyType)

    if lang == config.FRENCH:
        title = "Type de miel"
        description = ("Les différents types de miel que "
                       "vous pouvez être amené à récolter")
    else:
        title = "Honey type"
        description = ("The different kind of honey "
                       "that you are harvesting")

    return render("akingbee/setup/setup.html",
                  object_data=honey_types,
                  columns=('fr', 'en'),
                  menu=menu,
                  title=title,
                  id_title=id_title,
                  description=description)


@route("/setup/beehouse/actions", methods=['GET'])
@login_required
def setupBh_actions():
    lang = flask.session['language']
    menu = 4
    id_title = 'beehouse_actions'

    beehouse_actions = factory.get_all(objects.BeehouseAction)

    if lang == config.FRENCH:
        title = "Actions relatives aux ruches"
        description = ("Les différentes actions que vous "
                       "pouvez être amené à faire sur une ruche")
    else:
        title = "Beehouse actions"
        description = ("The différent actions that "
                       "you may have to do on a beehouse")

    return render("akingbee/setup/setup.html",
                  object_data=beehouse_actions,
                  columns=('fr', 'en'),
                  menu=menu,
                  title=title,
                  id_title=id_title,
                  descrition=description)



@route("/setup/apiary/status", methods=['GET'])
@login_required
def setupStatusAp():
    lang = flask.session['language']
    menu = 5
    id_title = 'status_apiary'

    apiary_statuses = factory.get_all(objects.StatusApiary)

    if lang == config.FRENCH:
        title = "Status des ruchers"
        description = ("Les différents status que vous "
                       "pouvez donner à un rucher")
    else:
        title = "Apiary status"
        description = ("The different status that "
                       "you may have to give to an apiary")

    return render("akingbee/setup/setup.html",
                  object_data=apiary_statuses,
                  columns=('fr', 'en'),
                  menu=menu,
                  title=title,
                  id_title=id_title,
                  description=description)


@route("/apiary/index/get_apiary_info", methods=['POST'])
@login_required
def apiary_details():
    ap_id = flask.request.form.get('ap_id')
    apiary = factory.get_from_id(ap_id, objects.Apiary)
    return flask.jsonify(apiary.serialize())


@route("/apiary/index/submit_apiary_info", methods=['POST'])
@login_required
def submit_apiary_details():
    ap_id = flask.request.form.get('ap_id')

    apiary = factory.get_from_id(ap_id, objects.Apiary)

    apiary.name = flask.request.form.get('name')
    apiary.location = flask.request.form.get('location')
    apiary.status = flask.request.form.get('status')
    apiary.honey_type = flask.request.form.get('honey')

    apiary.save()

    return Success(alerts.MODIFICATION_SUCCESS)


@route("/apiary/delete", methods=['POST'])
@login_required
def del_apiary():
    ap_id = flask.request.form.get('ap_id')

    apiary = factory.get_from_id(ap_id, objects.Apiary)
    apiary.delete()

    return Success(alerts.DELETION_SUCCESS)


