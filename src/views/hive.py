import datetime

import flask
from peewee import IntegrityError, DoesNotExist, JOIN

from src.database import DB
from src.helpers.tools import (
    render,
    get_all,
    login_required,
    update_hive_history,
)
from src.helpers.date import convert_to_date_object
from src.constants import config
from src.constants import alert_codes as alerts
from src.services.alerts import Error, Success
from src.constants.trad_codes import traductions

from src.models import (
    Hive,
    Apiary,
    Owner,
    HiveCondition,
    Swarm,
    SwarmHealth,
    Comment,
    CommentType,
    Action,
    ActionType,
)


api = flask.Blueprint("Hive", __name__)


@api.route("/hive", methods=["GET"])
@login_required
def hive_index():
    if flask.request.method == "GET":
        hives = get_all(Hive, Apiary, Owner, HiveCondition)
        apiaries = get_all(Apiary)
        owners = get_all(Owner)
        hive_conditions = get_all(HiveCondition)

        return render(
            "akingbee/hive/index.html",
            hives=hives,
            apiaries=apiaries,
            hive_conditions=hive_conditions,
            owners=owners,
        )


@api.route("/hive/create", methods=["GET"])
@login_required
def hive_create():
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


@api.route("/api/hive/<int:hive_id>", methods=["GET", "PUT", "DEL"])
@login_required
def hive_details(hive_id):
    try:
        hive = Hive.get_by_id(hive_id)
    except DoesNotExist:
        flask.abort(404)

    if flask.request.method == "GET":
        return flask.jsonify(hive.serialize())

    elif flask.request.method == "PUT":
        name = flask.request.form.get("hive")
        owner = flask.request.form.get("owner")

        if not name or not owner:
            raise Error(alerts.EMPTY_FIELD)

        try:
            hive.name = name
            hive.owner = owner
            hive.save()
        except IntegrityError:
            raise Error(alerts.INCONSISTANT_DATA)

        return Success(alerts.MODIFICATION_SUCCESS)

    elif flask.request.method == "DEL":
        hive.delete_instance()
        return Success(alerts.DELETION_SUCCESS)

@api.route("/api/hive", methods=["POST"])
def create_hive_api():
    hive_data = {
        "name": flask.request.form.get("name") or None,
        "birthday": convert_to_date_object(flask.request.form.get("date")),
        "apiary": flask.request.form.get("apiary"),
        "owner": flask.request.form.get("owner"),
        "condition": flask.request.form.get("hive_condition"),
    }

    swarm_health = flask.request.form.get("swarm_health")

    try:
        with DB.atomic():
            if swarm_health:
                swarm = Swarm(
                    health=swarm_health, birthday=datetime.datetime.now()
                )
                swarm.save()
                hive_data["swarm_id"] = swarm.id

            hive = Hive(**hive_data)
            hive.save()
    except IntegrityError:
        raise Error(alerts.INCONSISTANT_DATA)

    return Success(alerts.NEW_HIVE_SUCCESS)


@api.route("/api/comment", methods=["POST"])
@login_required
def create_a_comment():
    hive = Hive.get_by_id(flask.request.form.get("hive_id"))
    comment_data = {
        "hive": hive.id,
        "apiary": hive.apiary,
        "swarm": hive.swarm,
        "date": convert_to_date_object(flask.request.form.get("date")),
        "comment": flask.request.form.get("comment"),
        "health": flask.request.form.get("health"),
        "condition": flask.request.form.get("condition"),
        "type": config.COMMENT_TYPE_USER,
    }

    comment = Comment(**comment_data)
    comment.save()

    update_hive_history(hive)

    return Success(alerts.MODIFICATION_SUCCESS)


@api.route("/api/action", methods=["POST"])
@login_required
def create_action():
    data = {
        "hive": flask.request.form.get("hive_id"),
        "date": convert_to_date_object(flask.request.form.get("date")),
        "note": flask.request.form.get("note"),
        "type_id": flask.request.form.get("action_type"),
        "deadline": convert_to_date_object(flask.request.form.get("deadline")),
        "status": config.STATUS_PENDING,
    }

    action = Action(**data)
    action.save()

    return Success(alerts.ACTION_PLANIFICATION_SUCCESS)

@api.route("/api/action/<int:action_id>", methods=["PUT"])
@login_required
def update_action(action_id):
    action = Action.get_by_id(action_id)
    hive = Hive.get_by_id(action.hive)

    data = {
        "date": convert_to_date_object(flask.request.form.get("date")),
        "action": action.id,
        "hive": hive.id,
        "apiary": hive.apiary,
        "type": config.COMMENT_TYPE_ACTION,
    }

    text = flask.request.form.get('name')
    if flask.request.form.get("description"):
        text += f" - {flask.request.form['description']}"
    data["comment"] = text

    comment = Comment(**data)
    comment.save()

    action.date_done = data["date"]
    action.status = config.STATUS_DONE
    action.save()

    return Success(alerts.ACTION_SOLVED_SUCCESS)



@api.route("/hive/<int:hive_id>", methods=["GET"])
@login_required
def hive_profil(hive_id):

    try:
        hive = Hive.get_by_id(hive_id)
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
        .where(Comment.hive_id == hive_id)
        .order_by(Comment.date.desc())
    )

    comment_types = tuple(set(comment.type for comment in comments))

    actions = Action.select().where(
        Action.hive == hive_id and Action.status == config.STATUS_PENDING
    )

    hive_conditions = get_all(HiveCondition)
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
        hive_conditions=hive_conditions,
        apiaries=apiaries,
        swarm_healths=swarm_healths,
        owners=owners,
        action_types=action_types,
    )


@api.route("/api/hive/<int:hive_id>/<string:way>", methods=["GET"])
@login_required
def select_hive(hive_id, way):
    if way not in ("next", "prev"):
        flask.abort(404)

    hives = [hive.id for hive in get_all(Hive)]
    index = hives.index(hive_id)

    inc = 1 if way == "next" else -1
    new_id = hives[(index + inc) % len(hives)]

    return flask.jsonify(f"/hive/{new_id}")



@api.route("/api/comment/<int:comment_id>", methods=["DEL", "PUT"])
@login_required
def operate_comment(comment_id):
    if flask.request.method == "PUT":
        comment = Comment.get_by_id(comment_id)

        comment.comment = flask.request.form.get("comment")
        comment.health = flask.request.form.get("health")
        comment.condition = flask.request.form.get("condition")
        comment.date = convert_to_date_object(flask.request.form.get("date"))
        comment.save()

        hive = Hive.get_by_id(comment.hive)
        update_hive_history(hive)

        return Success(alerts.MODIFICATION_SUCCESS)

    elif flask.request.method == "DEL":
        comment = Comment.get_by_id(comment_id)

        if comment.type.id == config.COMMENT_TYPE_ACTION:
            action = Action.get_by_id(comment.action)
            action.status = config.STATUS_PENDING
            action.date_done = None
            action.save()

        hive = Hive.get_by_id(comment.hive)
        comment.delete_instance()

        update_hive_history(hive)

        return Success(alerts.DELETION_SUCCESS)


