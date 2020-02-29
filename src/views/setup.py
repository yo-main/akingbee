import flask
import peewee

from src.helpers.tools import login_required, render, get_all
from src.errors import errors
from src.success import success

from src.models import (
    Owner,
    HiveCondition,
    HoneyType,
    EventType,
    SwarmHealth,
    StatusApiary,
)


api = flask.Blueprint("Setup", __name__)


REFS = {
    "owner": {"object": Owner, "title": 40},
    "conditions": {"object": HiveCondition, "title": 114},
    "honey": {"object": HoneyType, "title": 27},
    "events": {"object": EventType, "title": 119},
    "status": {"object": StatusApiary, "title": 118},
    "health": {"object": SwarmHealth, "title": 113},
}


@api.route("/setup", methods=["GET"])
@login_required
def setupPage():
    if flask.request.method == "GET":
        return render("akingbee/setup/index.html", objects=None, title_id=None)


@api.route(
    "/setup/<string:entity>/<string:data_name>",
    methods=["GET", "POST", "PUT", "DELETE"],
)
@login_required
def submit_new_data(entity, data_name):
    if data_name not in REFS:
        flask.abort(404)
    class_ = REFS[data_name]["object"]

    if flask.request.method == "POST":
        data = flask.request.form.get("data")

        if not data:
            raise errors.MissingInformation()

        if class_ == Owner:
            obj = class_(**{"name": data})
        else:
            obj = class_(**{"fr": data, "en": data})

        obj.save()

        return success.NewParameterSuccess()

    elif flask.request.method == "PUT":
        data_id = flask.request.form.get("id")
        data = flask.request.form.get("data")
        obj = class_.get_by_id(data_id)

        if not data:
            raise errors.MissingInformation()

        if class_ == Owner:
            obj.name = data
        else:
            obj.fr = data
            obj.en = data

        obj.save()

        return success.ModificationSuccess()

    elif flask.request.method == "DELETE":
        data_id = flask.request.form.get("id")
        obj = class_.get_by_id(data_id)
        try:
            obj.delete_instance()
        except peewee.IntegrityError:
            raise errors.DeleteIntegrityError()

        return success.DeletionSuccess()

    elif flask.request.method == "GET":
        return render(
            "akingbee/setup/index.html",
            objects=get_all(class_),
            column_name="name"
            if class_ == Owner
            else flask.session["language"],
            title_id=REFS[data_name]["title"],
        )
