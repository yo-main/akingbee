import datetime

import flask

from src.database import DB
from src.helpers.tools import login_required
from src.services.alerts import Error, Success
from src.constants import alert_codes as alerts

from src.models import Swarm


api = flask.Blueprint("Swarm", __name__)


@api.route("/swarm/create", methods=["POST"])
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
