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

import peewee as pw

from src.constants import config
from src.constants import environments
from src.constants import alert_codes as alerts

from src.constants.environments import USER_ID

# from src.data_access import objects
from src.data_access.pw_objects import User
from src.data_access.pw_objects import Hive
from src.data_access.pw_objects import Owner
from src.data_access.pw_objects import Swarm
from src.data_access.pw_objects import Action
from src.data_access.pw_objects import Apiary
from src.data_access.pw_objects import Comment
from src.data_access.pw_objects import HoneyType
from src.data_access.pw_objects import HiveCondition
from src.data_access.pw_objects import ActionType
from src.data_access.pw_objects import CommentType
from src.data_access.pw_objects import SwarmHealth
from src.data_access.pw_objects import StatusApiary

from src.data_access.connectors import DB
from src.helpers import helpers
from src.helpers.helpers import route
from src.helpers.helpers import get_all
from src.helpers.helpers import redirect
from src.helpers.helpers import login_required
from src.helpers.helpers import verify_password
from src.helpers.helpers import create_password_hash
from src.helpers.helpers import get_user_from_username
from src.helpers.checkers import validate_email
from src.helpers.checkers import validate_password
from src.services.logger import logger
from src.services.alerts import Error, Success
from src.helpers.date import convert_to_date_object


def render(url, **kwargs):
    if "language" not in flask.session:
        flask.session["language"] = config.FRENCH

    return flask.render_template(
        url,
        lang=flask.session["language"],
        trads=helpers.traductions(),
        url_root=environments.FLASK_URL_ROOT,
        **kwargs,
    )


@route("/", methods=["GET"])
@login_required
def home():
    return render("akingbee/index_akb.html")


@route("/images/<path:filename>", methods=["GET"])
def get_image(filename):
    filepath = os.path.join(environments.IMAGES_FOLDER, filename)
    if os.path.exists(filepath):
        return flask.send_file(filepath, mimetype="image/svg+xml")
    return flask.abort(404)


@route("/favicon.ico", methods=["GET"])
def get_favicon():
    filepath = os.path.join(os.getcwd(), "favicon.ico")
    if os.path.exists(filepath):
        return flask.send_file(filepath, mimetype="image/x-con")
    return flask.abort(404)


@route("/login", methods=["GET", "POST"])
def login():

    # We remove the user credentials if any in the cookie
    flask.session["user_id"] = None
    flask.session.pop("username", None)

    if flask.request.method == "GET":
        return render("akingbee/login.html")

    logger.info("Login attempt")

    username = flask.request.form.get("username")
    password = flask.request.form.get("password")

    user = get_user_from_username(username)

    # this variable should only be set to false in test
    if environments.PASSWORD_REQUESTED:
        if not verify_password(user.pwd, password):
            raise Error(alerts.INCORRECT_PASSWORD_ERROR)

        # All good ! We can log in the user
        user.date_last_connection = datetime.datetime.now()
        user.save()

    flask.session["user_id"] = user.id
    flask.session["username"] = user.username
    return Success(alerts.LOGIN_SUCCESS)


@route("/logout", methods=["GET"])
def logout():
    logger.info("Logout")
    flask.session["user_id"] = None
    flask.session.pop("username", None)
    return redirect("/")


@route("/language", methods=["POST"])
def updateLanguage():
    """Change the user language"""
    newLanguage = flask.request.form.get("language")

    if newLanguage not in config.LANGUAGES:
        newLanguage = config.ENGLISH

    flask.session["language"] = newLanguage
    return Success()


@route("/register", methods=["GET"])
def register():
    return render("akingbee/register.html")


@route("/registercheck", methods=["POST"])
def registerCheck():
    """
    Will check that we can correctly register a new user
    """
    logger.info("Registration attempt")

    data = {
        "pwd": flask.request.form.get("pwd"),
        "email": flask.request.form.get("email").lower(),
        "username": flask.request.form.get("username"),
    }

    if not validate_email(data["email"]):
        raise Error(alerts.INCORRECT_EMAIL_FORMAT)

    if not validate_password(data["pwd"]):
        raise Error(alerts.INCORRECT_PASSWORD_FORMAT)

    if not data["email"] or not data["username"]:
        raise Error(alerts.MISSING_INFORMATION_REGISTER)

    user = User.select().where(User.username == data["username"]).count()
    if user:
        raise Error(alerts.USER_ALREADY_EXISTS_ERROR)

    email = User.select().where(User.email == data["email"]).count()
    if email:
        raise Error(alerts.EMAIL_ALREADY_EXISTS_ERROR)

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

    return Success(alerts.REGISTER_SUCCESS)


@route("/reset_password", methods=["GET", "POST"])
def reset_pwd():
    if flask.session.get("user_id") is not None:
        return redirect("/")

    if flask.request.method == "GET":
        return render("akingbee/reset_pwd.html")

    if flask.request.method == "POST":
        pwd = flask.request.form.get("pwd")
        username = flask.request.form.get("username")

        if not validate_password(pwd):
            raise Error(alerts.INCORRECT_PASSWORD_FORMAT)

        hashed_pwd = create_password_hash(pwd)

        user = get_user_from_username(username)
        user.pwd = hashed_pwd
        user.save()

        return Success(alerts.PASSWORD_RESET_SUCCESS)


@route("/apiary", methods=["GET"])
@login_required
def apiary():
    apiaries = get_all(Apiary, StatusApiary, HoneyType)
    apiary_statuses = tuple(set(apiary.status for apiary in apiaries))
    honey_types = tuple(set(apiary.honey_type for apiary in apiaries))
    location_list = tuple(set(apiary.location for apiary in apiaries))

    return render(
        "akingbee/apiary/index.html",
        apiaries=apiaries,
        locations=location_list,
        apiary_statuses=apiary_statuses,
        honey_types=honey_types,
    )


@route("/apiary/create", methods=["GET", "POST"])
@login_required
def apiary_create():
    if flask.request.method == "GET":
        honey_types = get_all(HoneyType)
        apiary_statuses = get_all(StatusApiary)

        return render(
            "akingbee/apiary/create.html",
            honey_types=honey_types,
            apiary_statuses=apiary_statuses,
        )

    elif flask.request.method == "POST":
        data = {
            "name": flask.request.form.get("name"),
            "location": flask.request.form.get("location"),
            "honey_type": flask.request.form.get("honey_type"),
            "status": flask.request.form.get("status"),
            "birthday": convert_to_date_object(flask.request.form.get("birthday")),
        }

        apiary = Apiary(**data)
        apiary.save()

        return Success(alerts.NEW_APIARY_SUCCESS)


@route("/apiary/create/new_honey_type", methods=["POST"])
@login_required
def apiary_create_honey():
    data = {
        "fr": flask.request.form.get("name_fr"),
        "en": flask.request.form.get("name_en"),
    }

    honey = HoneyType(**data)
    honey.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@route("/apiary/create/new_apiary_status", methods=["POST"])
@login_required
def apiary_status_create():
    data = {
        "fr": flask.request.form.get("name_fr"),
        "en": flask.request.form.get("name_en"),
    }

    status_apiary = StatusApiary(**data)
    status_apiary.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@route("/hive", methods=["GET"])
@login_required
def hive():
    hives = get_all(Hive, Apiary, Owner, HiveCondition)
    apiaries = tuple(set(hive.apiary for hive in hives))
    owners = tuple(set(hive.owner for hive in hives))

    # Above fields will only show values already linked to a hive
    # However for the edit modal we need all conditions so we make a specific query
    # It's probably something we would need to do for the above value but it'll impact performance...
    hive_conditions = get_all(HiveCondition)

    return render(
        "akingbee/hive/index.html",
        hives=hives,
        apiaries=apiaries,
        hive_conditions=hive_conditions,
        owners=owners,
    )


@route("/hive/create", methods=["GET", "POST"])
@login_required
def hive_create():
    if flask.request.method == "GET":
        owners = get_all(Owner)
        apiaries = get_all(Apiary)
        hive_conditions = get_all(HiveCondition)
        swarm_healths = get_all(SwarmHealth)
        
        return render(
            "akingbee/hive/create.html",
            owners=owners,
            apiaries=apiaries,
            hive_conditions=hive_conditions,
            swarm_healths=swarm_healths
        )

    elif flask.request.method == "POST":
        hive_data = {
            "name": flask.request.form.get("name"),
            "birthday": convert_to_date_object(flask.request.form.get("date")),
            "apiary": flask.request.form.get("apiary"),
            "owner": flask.request.form.get("owner"),
            "condition": flask.request.form.get("hive_condition"),
        }

        with DB.atomic():
            swarm_health = flask.request.form.get("swarm_health")
            if swarm_health:
                swarm = Swarm(health=swarm_health,
                              birthday=datetime.datetime.now())
                swarm.save()
                hive_data["swarm_id"] = swarm.id

            hive = Hive(**hive_data)
            hive.save()

        return Success(alerts.NEW_HIVE_SUCCESS)


@route("/hive/create/new_owner", methods=["POST"])
@login_required
def hive_create_owner():
    data = {"name": flask.request.form.get("owner")}
    owner = Owner(**data)
    owner.save()

    return Success(alerts.NEW_BEEKEEPER_SUCCESS)


@route("/hive/create/new_condition", methods=["POST"])
@login_required
def hive_create_condition():
    data = {
        "fr": flask.request.form.get("name_fr"),
        "en": flask.request.form.get("name_en"),
    }
    hive_condition = HiveCondition(**data)
    hive_condition.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@route("/hive/get_hive_info", methods=["POST"])
@login_required
def hive_details():
    bh_id = flask.request.form.get("bh_id")
    hive = Hive.get_by_id(bh_id)
    return flask.jsonify(hive.serialize())


@route("/hive/submit_hive_info", methods=["POST"])
@login_required
def submit_hive_details():
    hive = Hive.get_by_id(flask.request.form.get("bh_id"))

    hive.apiary = flask.request.form.get("apiary")
    hive.name = flask.request.form.get("hive")
    hive.owner = flask.request.form.get("owner")
    # hive.condition = flask.request.form.get("condition")
    hive.save()

    return Success(alerts.MODIFICATION_SUCCESS)


@route("/hive/submit_comment_modal", methods=["POST"])
@login_required
def submit_comment_modal():
    hive = Hive.get_by_id(flask.request.form.get("bh_id"))
    comment_data = {
        "hive": hive.id,
        "apiary": hive.apiary,
        "swarm": hive.swarm,
        "date": convert_to_date_object(flask.request.form.get("date")),
        "comment": flask.request.form.get("comment"),
        "health": flask.request.form.get("health"),
        "type": config.COMMENT_TYPE_USER,
    }
    comment = Comment(**comment_data)
    comment.save()

    helpers.update_swarm_health(hive.swarm)

    return Success(alerts.MODIFICATION_SUCCESS)


@route("/hive/submit_action_modal", methods=["POST"])
@login_required
def submit_action_modal():
    data = {
        "hive": flask.request.form.get("bh_id"),
        "date": convert_to_date_object(flask.request.form.get("date")),
        "description": flask.request.form.get("description"),
        "type_id": flask.request.form.get("action_type"),
        "deadline": convert_to_date_object(flask.request.form.get("deadline")),
        "status": config.STATUS_PENDING,
    }
    action = Action(**data)
    action.save()

    return Success(alerts.ACTION_PLANIFICATION_SUCCESS)


@route("/hive/<path:bh_id>", methods=["GET"])
@login_required
def hive_profil(bh_id):

    try:
        hive = Hive.get_by_id(bh_id)
    except pw.DoesNotExist:
        flask.abort(404)

    if hive.user_id != flask.session["user_id"]:
        flask.abort(404)

    comments = (
        Comment
        .select(Comment, Hive, Apiary, CommentType)
        .join(Hive)
        .switch(Comment)
        .join(Apiary)
        .switch(Comment)
        .join(SwarmHealth, pw.JOIN.LEFT_OUTER)
        .switch(Comment)
        .join(CommentType)
        .where(Comment.hive_id == bh_id)
        .order_by(Comment.date.desc())
    )

    comment_types = tuple(set(comment.type for comment in comments))

    actions = Action.select().where(
        Action.hive == bh_id and Action.status == config.STATUS_PENDING
    )

    swarm_healths = get_all(SwarmHealth)
    action_types = get_all(ActionType)
    apiaries = get_all(Apiary)
    owners = get_all(Owner)
    
    return render(
        "akingbee/hive/hive_details.html",
        hive=hive,
        comments=comments,
        actions=actions,
        comment_types=comment_types,
        apiaries=apiaries,
        swarm_healths=swarm_healths,
        owners=owners,
        action_types=action_types,
    )


@route("/hive/select", methods=["POST"])
@login_required
def select_hive():
    bh_id = int(flask.request.form.get("bh_id"))
    way = int(flask.request.form.get("way"))

    hives = [hive.id for hive in get_all(Hive)]
    index = hives.index(bh_id)

    new_id = hives[(index + way) % len(hives)]

    return flask.jsonify(f"/hive/{new_id}")


@route("/hive/submit_solve_action_modal", methods=["POST"])
@login_required
def solve_action():

    action = Action.get_by_id(flask.request.form.get("ac_id"))
    hive = Hive.get_by_id(action.hive)

    data = {
        "comment": flask.request.form.get("description"),
        "date": convert_to_date_object(flask.request.form.get("date")),
        "action": action.id,
        "hive": hive.id,
        "apiary": hive.apiary,
        "type": config.COMMENT_TYPE_ACTION,
    }

    comment = Comment(**data)
    comment.save()

    action.date_done = data["date"]
    action.status = config.STATUS_DONE
    action.save()

    return Success(alerts.ACTION_SOLVED_SUCCESS)


@route("/hive/submit_edit_comment_modal", methods=["POST"])
@login_required
def edit_comment():
    comment = Comment.get_by_id(flask.request.form.get("cm_id"))

    comment.comment = flask.request.form.get("comment")
    comment.health = flask.request.form.get("health")
    comment.date = convert_to_date_object(flask.request.form.get("date"))
    comment.save()

    helpers.update_swarm_health(comment.swarm)

    return Success(alerts.MODIFICATION_SUCCESS)


@route("/hive/delete_comment", methods=["POST"])
@login_required
def del_comment():
    comment = Comment.get_by_id(flask.request.form.get("cm_id"))

    if comment.type == config.COMMENT_TYPE_ACTION:
        action = Action.get_by_id(comment.action)
        action.status = config.STATUS_PENDING
        action.date_done = None
        action.save()

    swarm_id = comment.swarm
    comment.delete_instance()
    
    helpers.update_swarm_health(swarm_id)

    return Success(alerts.DELETION_SUCCESS)


@route("/setup", methods=["GET"])
@login_required
def setupPage():
    if flask.request.method == "GET":
        return render("akingbee/setup/index.html", title=0, column="")


@route("/setup/update", methods=["POST"])
@login_required
def submit_data():
    fr = flask.request.form.get("fr")
    en = flask.request.form.get("en")
    data_id = flask.request.form.get("dataId")
    source = flask.request.form.get("source")

    if "/setup/hive/owner" in source:
        obj = Owner.get_by_id(data_id)
        obj.name = fr
    elif "/setup/hive/conditions" in source:
        obj = HiveCondition.get_by_id(data_id)
        obj.fr = fr
        obj.en = en
    elif "/setup/hive/honey" in source:
        obj = HoneyType.get_by_id(data_id)
        obj.fr = fr
        obj.en = en
    elif "/setup/hive/actions" in source:
        obj = ActionType.get_by_id(data_id)
        obj.fr = fr
        obj.en = en
    elif "/setup/apiary/status" in source:
        obj = StatusApiary.get_by_id(data_id)
        obj.fr = fr
        obj.en = en
    elif "setup/swarm/health" in source:
        obj = SwarmHealth.get_by_id(data_id)
        obj.fr = fr
        obj.en = en
    else:
        raise Error(alerts.INTERNAL_ERROR)

    obj.save()

    return Success(alerts.MODIFICATION_SUCCESS)


@route("/setup/delete", methods=["POST"])
@login_required
def delete_data():
    data_id = flask.request.form.get("dataId")
    source = flask.request.form.get("source")

    if "/setup/hive/owner" in source:
        obj = Owner.get_by_id(data_id)
    elif "/setup/hive/conditions" in source:
        obj = HiveCondition.get_by_id(data_id)
    elif "/setup/hive/honey" in source:
        obj = HoneyType.get_by_id(data_id)
    elif "/setup/hive/actions" in source:
        obj = ActionType.get_by_id(data_id)
    elif "/setup/apiary/status" in source:
        obj = StatusApiary.get_by_id(data_id)
    elif "setup/swarm/health" in source:
        obj = SwarmHealth.get_by_id(data_id)
    else:
        raise Error(alerts.INTERNAL_ERROR)

    obj.delete_instance()

    return Success(alerts.DELETION_SUCCESS)


@route("/setup/submit", methods=["POST"])
@login_required
def submit_new_data():
    fr = flask.request.form.get("fr")
    en = flask.request.form.get("en")
    source = flask.request.form.get("source")

    if "/setup/hive/owner" in source:
        obj = Owner(**{"name": fr})
    elif "/setup/hive/conditions" in source:
        obj = HiveCondition(**{"fr": fr, "en": en})
    elif "/setup/hive/honey" in source:
        obj = HoneyType(**{"fr": fr, "en": en})
    elif "/setup/hive/actions" in source:
        obj = ActionType(**{"fr": fr, "en": en})
    elif "/setup/apiary/status" in source:
        obj = StatusApiary(**{"fr": fr, "en": en})
    elif "/setup/swarm/health" in source:
        obj = SwarmHealth(**{"fr": fr, "en": en})
    else:
        raise Error(alerts.INTERNAL_ERROR)

    obj.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@route("/setup/hive/owner", methods=["GET"])
@login_required
def setupOwner():
    lang = flask.session["language"]
    menu = 1
    id_title = "owner"

    owners = get_all(Owner)

    if lang == config.FRENCH:
        title = "Apiculteur"
        description = (
            "L'apiculteur d'une ruche (juste au cas "
            "où vous gérez les ruches d'une autre personne)"
        )
    else:
        title = "Beekeeper"
        description = (
            "The beekeper of a hive (in case "
            "you manage hive on behalf of other people ?)"
        )

    return render(
        "akingbee/setup/index.html",
        object_data=owners,
        column="name",
        menu=menu,
        title=title,
        id_title=id_title,
        description=description,
    )


@route("/setup/hive/conditions", methods=["GET"])
@login_required
def setupCondition():
    lang = flask.session["language"]
    menu = 2
    id_title = "condition"

    hive_conditions = get_all(HiveCondition)

    if lang == config.FRENCH:
        title = "États"
        description = (
            "Les différents états que vous souhaitez affecter à une ruche"
        )
    else:
        title = "Conditions"
        description = "Different conditions that you wish to affect to a hive"

    return render(
        "akingbee/setup/index.html",
        object_data=hive_conditions,
        column=lang,
        menu=menu,
        title=title,
        id_title=id_title,
        description=description,
    )


@route("/setup/hive/honey", methods=["GET"])
@login_required
def setupHoneyKind():
    lang = flask.session["language"]
    menu = 3
    id_title = "honey_type"

    honey_types = get_all(HoneyType)

    if lang == config.FRENCH:
        title = "Type de miel"
        description = (
            "Les différents types de miel que "
            "vous pouvez être amené à récolter"
        )
    else:
        title = "Honey type"
        description = "The different kind of honey " "that you are harvesting"

    return render(
        "akingbee/setup/index.html",
        object_data=honey_types,
        column=lang,
        menu=menu,
        title=title,
        id_title=id_title,
        description=description,
    )


@route("/setup/hive/actions", methods=["GET"])
@login_required
def setupBh_actions():
    lang = flask.session["language"]
    menu = 4
    id_title = "action_types"

    action_types = get_all(ActionType)

    if lang == config.FRENCH:
        title = "Type d'actions"
        description = (
            "Les différentes actions que vous "
            "pouvez être amené à faire sur une ruche"
        )
    else:
        title = "Action types"
        description = "The different actions that you may have to do on a hive"

    return render(
        "akingbee/setup/index.html",
        object_data=action_types,
        column=lang,
        menu=menu,
        title=title,
        id_title=id_title,
        descrition=description,
    )


@route("/setup/apiary/status", methods=["GET"])
@login_required
def setupStatusAp():
    lang = flask.session["language"]
    menu = 5
    id_title = "status_apiary"

    apiary_statuses = get_all(StatusApiary)

    if lang == config.FRENCH:
        title = "Status des ruchers"
        description = (
            "Les différents status que vous pouvez donner à un rucher"
        )
    else:
        title = "Apiary status"
        description = (
            "The different status that you may have to give to an apiary"
        )

    return render(
        "akingbee/setup/index.html",
        object_data=apiary_statuses,
        column=lang,
        menu=menu,
        title=title,
        id_title=id_title,
        description=description,
    )


@route("/apiary/get_apiary_info", methods=["POST"])
@login_required
def apiary_details():
    ap_id = flask.request.form.get("ap_id")
    apiary = Apiary.get_by_id(ap_id)
    return flask.jsonify(apiary.serialize())


@route("/apiary/submit_apiary_info", methods=["POST"])
@login_required
def submit_apiary_details():
    ap_id = flask.request.form.get("ap_id")

    apiary = Apiary.get_by_id(ap_id)

    apiary.name = flask.request.form.get("name")
    apiary.location = flask.request.form.get("location")
    apiary.status = flask.request.form.get("status")
    apiary.honey_type = flask.request.form.get("honey")

    apiary.save()

    return Success(alerts.MODIFICATION_SUCCESS)


@route("/apiary/delete", methods=["POST"])
@login_required
def del_apiary():
    ap_id = flask.request.form.get("ap_id")

    apiary = Apiary.get_by_id(ap_id)
    apiary.delete_instance()

    return Success(alerts.DELETION_SUCCESS)


@route("/hive/delete", methods=["POST"])
@login_required
def delete_hive():
    hive_id = flask.request.form.get("bh_id")
    hive = Hive.get_by_id(hive_id)

    hive.delete_instance()

    return Success(alerts.DELETION_SUCCESS)


# @route("/swarm", methods=["GET"])
# def swarm_index():
#     swarms = get_all(Swarm, Hive, SwarmHealth)
#     hives = tuple(set(swarm.hive for swarm in swarms))
#     healths = tuple(set(swarm.health for swarm in swarms))

#     return render(
#         "akingbee/swarm/index.html",
#         swarms=swarms,
#         hives=hives,
#         healths=healths,
#     )


# @route("/swarm/create", methods=["GET", "POST"])
# @login_required
# def create_swarm():
#     if flask.request.method == "GET":
#         apiaries = get_all(Apiary)
#         hives = get_all(Hive)
#         healths = get_all(SwarmHealth)

#         return render(
#             "akingbee/swarm/create.html",
#             hives=hives,
#             apiaries=apiaries,
#             healths=healths,
#         )

#     elif flask.request.method == "POST":
#         data = {
#             "name": flask.request.form.get("name"),
#             "hive": flask.request.form.get("hive"),
#             "health": flask.request.form.get("health"),
#             "birthday": convert_to_date(flask.request.form.get("birthday")),
#         }

#         data["apiary"] = tuple(Apiary
#                                .select(Apiary)
#                                .join(Hive)
#                                .where(Hive.id == data["hive"]))[0]
#         swarm = Swarm(**data)
#         swarm.save()

#         return Success(alerts.NEW_SWARM_SUCCESS)


@route("/setup/swarm/health", methods=["GET"])
@login_required
def setupSwarmHealth():
    lang = flask.session["language"]
    menu = 3
    id_title = "swarm_health"

    swarm_health = get_all(SwarmHealth)

    if lang == config.FRENCH:
        title = "Status de santé d'un essaim"
        description = (
            "Les différents status de santé que "
            "qui peuvent être associés à un essaim"
        )
    else:
        title = "Swarm health status"
        description = (
            "The different kind of health conditions "
            "that may be linked to a swarm"
        )

    return render(
        "akingbee/setup/index.html",
        object_data=swarm_health,
        column=lang,
        menu=menu,
        title=title,
        id_title=id_title,
        description=description,
    )


@route("/swarm/create", methods=["POST"])
@login_required
def create_swarm():
    hive_id = flask.request.form.get("hive_id")
    swarm_health = flask.request.form.get("swarm_health")

    hive = Hive.get_by_id(hive_id)
    
    if hive.swarm:
        raise Error(alerts.SWARM_ALREADY_EXISTS)
    
    swarm = Swarm()
    swarm.user = flask.session["user_id"]
    swarm.health_id = swarm_health
    swarm.birthday = datetime.datetime.now()
    
    hive.swarm = swarm
    
    with DB.atomic():
        swarm.save()
        hive.save()
        
    return Success(alerts.SWARM_ATTACH_WITH_SUCCESS)

    
# @route("/swarm/get_swarm_info", methods=["POST"])
# @login_required
# def swarm_details():
#     swarm_id = flask.request.form.get("swarm_id")
#     print(swarm_id)
#     swarm = Swarm.get_by_id(swarm_id)
#     return flask.jsonify(swarm.serialize())


# @route("/swarm/submit_swarm_info", methods=["POST"])
# @login_required
# def submit_swarm_details():
#     swarm = Swarm.get_by_id(flask.request.form.get("swarm_id"))

#     swarm.name = flask.request.form.get("name")
#     swarm.hive = flask.request.form.get("hive")
#     swarm.health = flask.request.form.get("health")
#     swarm.save()

#     return Success(alerts.MODIFICATION_SUCCESS)



