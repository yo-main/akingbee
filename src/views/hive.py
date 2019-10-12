import datetime

import flask
from peewee import IntegrityError, DoesNotExist, JOIN

from src.database import DB
from src.helpers.tools import render, get_all, login_required
from src.helpers.date import convert_to_date_object
from src.helpers.swarm import update_swarm_health
from src.constants import config
from src.constants import alert_codes as alerts
from src.services.alerts import Error, Success

from src.models import Hive, Apiary, Owner, HiveCondition, Swarm, SwarmHealth, Comment, CommentType, Action, ActionType


api = flask.Blueprint("Hive", __name__)


@api.route("/hive", methods=["GET"])
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


@api.route("/hive/create", methods=["GET", "POST"])
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
            swarm_healths=swarm_healths,
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
                swarm = Swarm(
                    health=swarm_health, birthday=datetime.datetime.now()
                )
                swarm.save()
                hive_data["swarm_id"] = swarm.id

            hive = Hive(**hive_data)
            hive.save()

        return Success(alerts.NEW_HIVE_SUCCESS)


@api.route("/hive/create/new_owner", methods=["POST"])
@login_required
def hive_create_owner():
    data = {"name": flask.request.form.get("owner")}
    owner = Owner(**data)
    owner.save()

    return Success(alerts.NEW_BEEKEEPER_SUCCESS)


@api.route("/hive/create/new_condition", methods=["POST"])
@login_required
def hive_create_condition():
    data = {
        "fr": flask.request.form.get("name_fr"),
        "en": flask.request.form.get("name_en"),
    }
    hive_condition = HiveCondition(**data)
    hive_condition.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@api.route("/hive/get_hive_info", methods=["POST"])
@login_required
def hive_details():
    bh_id = flask.request.form.get("bh_id")
    hive = Hive.get_by_id(bh_id)
    return flask.jsonify(hive.serialize())


@api.route("/hive/submit_hive_info", methods=["POST"])
@login_required
def submit_hive_details():
    hive = Hive.get_by_id(flask.request.form.get("bh_id"))

    hive.apiary = flask.request.form.get("apiary")
    hive.name = flask.request.form.get("hive")
    hive.owner = flask.request.form.get("owner")
    # hive.condition = flask.request.form.get("condition")
    hive.save()

    return Success(alerts.MODIFICATION_SUCCESS)


@api.route("/hive/submit_comment_modal", methods=["POST"])
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

    update_swarm_health(hive.swarm)

    return Success(alerts.MODIFICATION_SUCCESS)


@api.route("/hive/submit_action_modal", methods=["POST"])
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


@api.route("/hive/<path:bh_id>", methods=["GET"])
@login_required
def hive_profil(bh_id):

    try:
        hive = Hive.get_by_id(bh_id)
    except DoesNotExist:
        flask.abort(404)

    if hive.user_id != flask.session["user_id"]:
        flask.abort(404)

    comments = (
        Comment.select(Comment, Hive, Apiary, CommentType)
        .join(Hive)
        .switch(Comment)
        .join(Apiary)
        .switch(Comment)
        .join(SwarmHealth, JOIN.LEFT_OUTER)
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


@api.route("/hive/select", methods=["POST"])
@login_required
def select_hive():
    bh_id = int(flask.request.form.get("bh_id"))
    way = int(flask.request.form.get("way"))

    hives = [hive.id for hive in get_all(Hive)]
    index = hives.index(bh_id)

    new_id = hives[(index + way) % len(hives)]

    return flask.jsonify(f"/hive/{new_id}")


@api.route("/hive/submit_solve_action_modal", methods=["POST"])
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


@api.route("/hive/submit_edit_comment_modal", methods=["POST"])
@login_required
def edit_comment():
    comment = Comment.get_by_id(flask.request.form.get("cm_id"))

    comment.comment = flask.request.form.get("comment")
    comment.health = flask.request.form.get("health")
    comment.date = convert_to_date_object(flask.request.form.get("date"))
    comment.save()

    update_swarm_health(comment.swarm)

    return Success(alerts.MODIFICATION_SUCCESS)


@api.route("/hive/delete_comment", methods=["POST"])
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

    update_swarm_health(swarm_id)

    return Success(alerts.DELETION_SUCCESS)



@api.route("/hive/delete", methods=["POST"])
@login_required
def delete_hive():
    hive_id = flask.request.form.get("bh_id")
    hive = Hive.get_by_id(hive_id)

    hive.delete_instance()

    return Success(alerts.DELETION_SUCCESS)