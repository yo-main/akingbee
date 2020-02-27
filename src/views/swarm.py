import datetime

import flask

from src.database import DB
from src.helpers.tools import (
    login_required,
    create_system_comment_from_hive,
    get_traductions,
)
from src.services.alerts import Error, Success
from src.constants import alert_codes as alerts

from src.models import Swarm, Hive


api = flask.Blueprint("Swarm", __name__)


@api.route("/api/swarm", methods=["POST", "DELETE"])
@login_required
def swarm_action():

    if flask.request.method == "POST":
        hive_id = flask.request.form.get("hive_id")
        swarm_health = flask.request.form.get("swarm_health")

        hive_id = flask.request.form.get("hive_id")
        swarm_health = flask.request.form.get("swarm_health")

        hive = Hive.get_or_none(id=hive_id)
        if hive is None:
            raise Error(alerts.UNKNOWN_DATA)

        if hive.swarm:
            raise Error(alerts.SWARM_ALREADY_EXISTS)

        swarm = Swarm()
        swarm.user = flask.session["user_id"]
        swarm.health_id = swarm_health
        swarm.birthday = datetime.datetime.now()

        hive.swarm = swarm

        msg = get_traductions(123).format(hive_name=hive.name)
        comment = create_system_comment_from_hive(msg, hive)

        with DB.atomic():
            swarm.save()
            hive.save()
            comment.save()

        return Success(alerts.SWARM_ATTACH_WITH_SUCCESS)

    if flask.request.method == "DELETE":
        hive_id = flask.request.form.get("hive_id")
        hive = tuple(
            Hive.select(Hive, Swarm).join(Swarm).where(Hive.id == hive_id)
        )[0]
        hive.swarm, swarm = None, hive.swarm

        msg = get_traductions(124).format(hive_name=hive.name)
        comment = create_system_comment_from_hive(msg, hive)

        with DB.atomic():
            hive.save()
            swarm.delete_instance()
            comment.save()

        return Success(alerts.DELETION_SUCCESS)
