import flask

from peewee import IntegrityError, DoesNotExist

from src.helpers.tools import get_all, render, login_required
from src.helpers.date import convert_to_date_object
from src.services.alerts import Error, Success
from src.constants import alert_codes as alerts
from src.database import DB

from src.models import Apiary, StatusApiary, HoneyType

api = flask.Blueprint("Apiary", __name__)


@api.route("/apiary", methods=["GET"])
@login_required
def apiary():
    apiaries = get_all(Apiary, StatusApiary, HoneyType)
    apiary_statuses = get_all(StatusApiary)
    honey_types = get_all(HoneyType)
    location_list = tuple(set(apiary.location for apiary in apiaries))

    return render(
        "akingbee/apiary/index.html",
        apiaries=apiaries,
        locations=location_list,
        apiary_statuses=apiary_statuses,
        honey_types=honey_types,
    )


@api.route("/apiary/create", methods=["GET"])
@login_required
def apiary_create():
    honey_types = get_all(HoneyType)
    apiary_statuses = get_all(StatusApiary)

    return render(
        "akingbee/apiary/create.html",
        honey_types=honey_types,
        apiary_statuses=apiary_statuses,
    )


######


@api.route("/api/honey_type", methods=["POST"])
@login_required
def apiary_create_honey():
    value = flask.request.form.get("value")

    if not value:
        raise Error(alerts.INCONSISTANT_DATA)

    honey = HoneyType(fr=value, en=value)
    honey.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@api.route("/api/apiary_status", methods=["POST"])
@login_required
def apiary_status_create():
    value = flask.request.form.get("value")

    if not value:
        raise Error(alerts.INCONSISTANT_DATA)

    status_apiary = StatusApiary(fr=value, en=value)
    status_apiary.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@api.route("/api/apiary", methods=["POST"])
@login_required
def create_apiary_api():
    data = {
        "name": flask.request.form.get("name"),
        "location": flask.request.form.get("location"),
        "honey_type_id": flask.request.form.get("honey_type"),
        "status_id": flask.request.form.get("status"),
        "birthday": convert_to_date_object(flask.request.form.get("birthday")),
    }

    if not all(x for x in data.values()):
        raise Error(alerts.MISSING_INFORMATION_APIARY)

    try:
        apiary = Apiary(**data)
        apiary.save()
    except IntegrityError as e:
        raise Error(alerts.INCONSISTANT_DATA)

    return Success(alerts.NEW_APIARY_SUCCESS)


@api.route("/api/apiary/<path:apiary_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def apiary_details(apiary_id):
    try:
        apiary = Apiary.get_by_id(apiary_id)
    except DoesNotExist:
        flask.abort(404)

    if flask.request.method == "GET":
        return flask.jsonify(apiary.serialize())

    elif flask.request.method == "PUT":
        form = flask.request.form
        count = 0

        # or None is there to manage empty strings and raise a 500 error
        if "name" in form:
            apiary.name = form["name"]
            count += 1
        if "location" in form:
            apiary.location = form["location"]
            count += 1
        if "status" in form:
            apiary.status = form["status"]
            count += 1
        if "honey" in form:
            apiary.honey_type = form["honey"]
            count += 1

        if not count:
            raise Error(alerts.INCONSISTANT_DATA)

        apiary.save()
        return Success(alerts.MODIFICATION_SUCCESS)

    elif flask.request.method == "DELETE":
        with DB.atomic():
            for comment in apiary.comments:
                comment.apiary = None
                comment.save()

            try:
                apiary.delete_instance()
            except IntegrityError:
                raise Error(alerts.SQL_FOREIGN_KEY_ERROR)

        return Success(alerts.DELETION_SUCCESS)
