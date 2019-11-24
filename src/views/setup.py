import flask

from src.helpers.tools import login_required, render, get_all
from src.services.alerts import Error, Success
from src.constants import alert_codes as alerts
from src.constants import config

from src.models import (
    Owner,
    HiveCondition,
    HoneyType,
    ActionType,
    SwarmHealth,
    StatusApiary,
)


api = flask.Blueprint("Setup", __name__)


@api.route("/setup", methods=["GET"])
@login_required
def setupPage():
    if flask.request.method == "GET":
        return render("akingbee/setup/index.html", title=0, column="")


@api.route("/setup/update", methods=["POST"])
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


@api.route("/setup/delete", methods=["POST"])
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


@api.route("/setup/submit", methods=["POST"])
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


@api.route("/setup/hive/owner", methods=["GET"])
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


@api.route("/setup/hive/conditions", methods=["GET"])
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


@api.route("/setup/hive/honey", methods=["GET"])
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


@api.route("/setup/hive/actions", methods=["GET"])
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


@api.route("/setup/apiary/status", methods=["GET"])
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


@api.route("/setup/swarm/health", methods=["GET"])
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
