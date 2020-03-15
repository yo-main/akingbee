import flask

from peewee import IntegrityError, DoesNotExist

from common.database import DB
from common.models import Apiary, StatusApiary, HoneyType

from webapp.helpers.tools import get_all, render, login_required
from webapp.helpers.date import convert_to_date_object
from webapp.errors import errors
from webapp.success import success


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
        raise errors.MissingInformation()

    honey = HoneyType(fr=value, en=value)
    honey.save()

    return success.NewParameterSuccess()


@api.route("/api/apiary_status", methods=["POST"])
@login_required
def apiary_status_create():
    value = flask.request.form.get("value")

    if not value:
        raise errors.MissingInformation()

    status_apiary = StatusApiary(fr=value, en=value)
    status_apiary.save()

    return success.NewParameterSuccess()


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
        raise errors.MissingInformation()

    try:
        apiary = Apiary(**data)
        apiary.save()
    except IntegrityError as e:
        raise errors.SqlProcessingError

    return success.NewApiarySuccess()


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
            raise errors.MissingInformation()

        apiary.save()
        return success.ModificationSuccess()

    elif flask.request.method == "DELETE":
        with DB.atomic():
            for comment in apiary.comments:
                comment.apiary = None
                comment.save()

            try:
                apiary.delete_instance()
            except IntegrityError:
                raise errors.DeleteIntegrityError()

        return success.DeletionSuccess()
