import flask

from peewee import IntegrityError

from src.helpers.tools import get_all, render, login_required
from src.helpers.date import convert_to_date_object
from src.services.alerts import Error, Success
from src.constants import alert_codes as alerts

from src.models import Apiary, StatusApiary, HoneyType

api = flask.Blueprint("Apiary", __name__)


@api.route("/apiary", methods=["GET"])
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


@api.route("/apiary/create", methods=["GET", "POST"])
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
            "honey_type_id": flask.request.form.get("honey_type"),
            "status_id": flask.request.form.get("status"),
            "birthday": convert_to_date_object(
                flask.request.form.get("birthday")
            ),
        }

        if not all(x for x in data.values()):
            raise Error(alerts.MISSING_INFORMATION_APIARY)

        try:
            apiary = Apiary(**data)
            apiary.save()
        except IntegrityError as e:
            raise Error(alerts.INCONSISTANT_DATA)

        return Success(alerts.NEW_APIARY_SUCCESS)


@api.route("/apiary/create/new_honey_type", methods=["POST"])
@login_required
def apiary_create_honey():
    fr = flask.request.form.get("name_fr")
    en = flask.request.form.get("name_en")

    if not fr or not en:
        raise Error(alerts.INCONSISTANT_DATA)

    honey = HoneyType(fr=fr, en=en)
    honey.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)


@api.route("/apiary/create/new_apiary_status", methods=["POST"])
@login_required
def apiary_status_create():
    fr = flask.request.form.get("name_fr")
    en = flask.request.form.get("name_en")

    if not fr or not en:
        raise Error(alerts.INCONSISTANT_DATA)

    status_apiary = StatusApiary(fr=fr, en=en)
    status_apiary.save()

    return Success(alerts.NEW_PARAMETER_SUCCESS)



@api.route("/apiary/get_apiary_info", methods=["POST"])
@login_required
def apiary_details():
    ap_id = flask.request.form.get("ap_id")
    apiary = Apiary.get_by_id(ap_id)
    return flask.jsonify(apiary.serialize())


@api.route("/apiary/submit_apiary_info", methods=["POST"])
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


@api.route("/apiary/delete", methods=["POST"])
@login_required
def del_apiary():
    ap_id = flask.request.form.get("ap_id")

    apiary = Apiary.get_by_id(ap_id)
    apiary.delete_instance()

    return Success(alerts.DELETION_SUCCESS)
