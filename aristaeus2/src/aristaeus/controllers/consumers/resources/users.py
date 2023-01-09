import json
import logging

from aristaeus.controllers.consumers.dtos.users import UserCreated

logger = logging.getLogger(__name__)


def on_user_created(properties, body):
    payload = UserCreated(**json.loads(body))


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
