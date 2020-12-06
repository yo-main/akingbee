import json

from gaea.database import db
from gaea.log import logger
from gaea.models import (
    HoneyTypes,
    HiveConditions,
    SwarmHealthStatuses,
    EventTypes,
    EventStatuses,
)

from .constants import (
    LANGUAGES,
    DEFAULT_HIVE_CONDITIONS,
    DEFAULT_HONEY_TYPES,
    DEFAULT_SWARM_HEALTH_STATUSES,
    DEFAULT_EVENT_TYPES,
    DEFAULT_EVENT_STATUSES,
)


def initialize_user(properties, body):
    body = json.loads(body)
    user_id = body.get("user_id")
    language = body.get("language")

    if user_id is None:
        logger.error(
            "Incorrect message received: missing 'user_id' key",
            body=body,
            properties=properties,
        )
        return False

    if language is None:
        logger.error(
            "Incorrect message received: missing 'language' key",
            body=body,
            properties=properties,
        )
        return False
    elif language not in LANGUAGES:
        logger.error(f"Incorrect language: {body['languages']}")
        return False

    objects = [
        HiveConditions(name=item[language], user_id=user_id)
        for item in DEFAULT_HIVE_CONDITIONS
    ]
    objects.extend(
        HoneyTypes(name=item[language], user_id=user_id) for item in DEFAULT_HONEY_TYPES
    )
    objects.extend(
        SwarmHealthStatuses(name=item[language], user_id=user_id)
        for item in DEFAULT_SWARM_HEALTH_STATUSES
    )
    objects.extend(
        EventTypes(name=item[language], user_id=user_id) for item in DEFAULT_EVENT_TYPES
    )
    objects.extend(
        EventStatuses(name=item[language], user_id=user_id)
        for item in DEFAULT_EVENT_STATUSES
    )

    db_client = db()
    with db_client as session:
        session.bulk_save_objects(objects)
        session.commit()

    logger.info("Default data created for user", user_id=user_id)
    return True
