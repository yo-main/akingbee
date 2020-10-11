import uuid
import datetime

from gaea.models import (
    Users,
    Credentials,
    Owners,
    Swarms,
    SwarmHealthStatuses,
    Hives,
    HiveConditions,
    Apiaries,
    ApiaryStatuses,
    HoneyTypes,
    Comments,
    CommentTypes,
    Events,
    EventStatuses,
    EventTypes,
)


def generate_uuid(nb):
    return tuple(uuid.uuid4() for _ in range(nb))


USER_EMAIL = "coucou@cou.com"
USER_USERNAME = "coucou"
USER_PASSWORD = "password"
SWARM_HEALTH_STATUS_GOOD = "Good"
SWARM_HEALTH_STATUS_BAD = "Bad"
HIVES_CONDITION_NEW = "New"
HIVES_CONDITION_OLD = "Old"
APIARY_STATUS_ACTIVE = "Active"
APIARY_STATUS_INACTIVE = "Active"
COMMENT_TYPE_USER = "User"
COMMENT_TYPE_SYSTEM = "System"
EVENT_STATUS_PLANIFIED = "Planified"
EVENT_STATUS_DONE = "Done"
EVENT_TYPE_BURN_BEES = "Burn them all"
EVENT_TYPE_WATER_BEEHOUSE = "Water it"
EVENT_TYPE_FIND_NEW_BEEHOUSE = "Find new beehouse"
HONEY_TYPE_CHESTNUT = "Chestnut"
HONEY_TYPE_ALL_FLOWERS = "All flowers"
HONEY_TYPE_SUNFLOWER = "Sunflower"

IDS = {
    "Users": generate_uuid(1),
    "Credentials": generate_uuid(1),
    "Owners": generate_uuid(2),
    "Swarms": generate_uuid(3),
    "Hives": generate_uuid(3),
    "Apiaries": generate_uuid(3),
    "Swarm_health_statuses": generate_uuid(2),
    "Apiary_statuses": generate_uuid(2),
    "Honey_types": generate_uuid(3),
    "Hive_conditions": generate_uuid(2),
    "Comment_types": generate_uuid(2),
    "Event_types": generate_uuid(3),
    "Event_statuses": generate_uuid(2),
    "Events": generate_uuid(2),
}

DATASET = (
    Users(id=IDS["Users"][0], email=USER_EMAIL),
    Credentials(
        id=uuid.uuid4(),
        username=USER_USERNAME,
        password=b"password",
        user_id=IDS["Users"][0],
    ),
    Owners(id=IDS["Owners"][0], surname="owner1", user_id=IDS["Users"][0]),
    Owners(id=IDS["Owners"][1], surname="owner2", user_id=IDS["Users"][0]),
    SwarmHealthStatuses(
        id=IDS["Swarm_health_statuses"][0],
        name=SWARM_HEALTH_STATUS_GOOD,
        user_id=IDS["Users"][0],
    ),
    SwarmHealthStatuses(
        id=IDS["Swarm_health_statuses"][1],
        name=SWARM_HEALTH_STATUS_BAD,
        user_id=IDS["Users"][0],
    ),
    Swarms(
        id=IDS["Swarms"][0],
        health_status_id=IDS["Swarm_health_statuses"][0],
        user_id=IDS["Users"][0],
    ),
    Swarms(
        id=IDS["Swarms"][1],
        health_status_id=IDS["Swarm_health_statuses"][0],
        user_id=IDS["Users"][0],
    ),
    Swarms(
        id=IDS["Swarms"][2],
        health_status_id=IDS["Swarm_health_statuses"][1],
        user_id=IDS["Users"][0],
    ),
    ApiaryStatuses(
        id=IDS["Apiary_statuses"][0], name=APIARY_STATUS_ACTIVE, user_id=IDS["Users"][0]
    ),
    ApiaryStatuses(
        id=IDS["Apiary_statuses"][1],
        name=APIARY_STATUS_INACTIVE,
        user_id=IDS["Users"][0],
    ),
    HoneyTypes(
        id=IDS["Honey_types"][0], name=HONEY_TYPE_ALL_FLOWERS, user_id=IDS["Users"][0]
    ),
    HoneyTypes(
        id=IDS["Honey_types"][1], name=HONEY_TYPE_CHESTNUT, user_id=IDS["Users"][0]
    ),
    HoneyTypes(
        id=IDS["Honey_types"][2], name=HONEY_TYPE_SUNFLOWER, user_id=IDS["Users"][0]
    ),
    Apiaries(
        id=IDS["Apiaries"][0],
        name="apiary1",
        location="location1",
        user_id=IDS["Users"][0],
        status_id=IDS["Apiary_statuses"][0],
        honey_type_id=IDS["Honey_types"][0],
    ),
    Apiaries(
        id=IDS["Apiaries"][1],
        name="apiary2",
        location="location2",
        user_id=IDS["Users"][0],
        status_id=IDS["Apiary_statuses"][0],
        honey_type_id=IDS["Honey_types"][1],
    ),
    Apiaries(
        id=IDS["Apiaries"][2],
        name="apiary3",
        location="location3",
        user_id=IDS["Users"][0],
        status_id=IDS["Apiary_statuses"][1],
        honey_type_id=IDS["Honey_types"][2],
    ),
    HiveConditions(
        id=IDS["Hive_conditions"][0], name=HIVES_CONDITION_NEW, user_id=IDS["Users"][0]
    ),
    HiveConditions(
        id=IDS["Hive_conditions"][1], name=HIVES_CONDITION_OLD, user_id=IDS["Users"][0]
    ),
    Hives(
        id=IDS["Hives"][0],
        name="hive1",
        user_id=IDS["Users"][0],
        condition_id=IDS["Hive_conditions"][0],
        owner_id=IDS["Owners"][0],
        swarm_id=IDS["Swarms"][0],
        apiary_id=IDS["Apiaries"][0],
    ),
    Hives(
        id=IDS["Hives"][1],
        name="hive2",
        user_id=IDS["Users"][0],
        condition_id=IDS["Hive_conditions"][0],
        owner_id=IDS["Owners"][1],
        swarm_id=IDS["Swarms"][1],
        apiary_id=IDS["Apiaries"][1],
    ),
    Hives(
        id=IDS["Hives"][2],
        name="hive3",
        user_id=IDS["Users"][0],
        condition_id=IDS["Hive_conditions"][1],
        owner_id=IDS["Owners"][0],
        swarm_id=IDS["Swarms"][2],
        apiary_id=IDS["Apiaries"][2],
    ),
    EventTypes(
        id=IDS["Event_types"][0], name=EVENT_TYPE_BURN_BEES, user_id=IDS["Users"][0]
    ),
    EventTypes(
        id=IDS["Event_types"][1],
        name=EVENT_TYPE_WATER_BEEHOUSE,
        user_id=IDS["Users"][0],
    ),
    EventTypes(
        id=IDS["Event_types"][2],
        name=EVENT_TYPE_FIND_NEW_BEEHOUSE,
        user_id=IDS["Users"][0],
    ),
    EventStatuses(
        id=IDS["Event_statuses"][0],
        name=EVENT_STATUS_PLANIFIED,
        user_id=IDS["Users"][0],
    ),
    EventStatuses(
        id=IDS["Event_statuses"][1], name=EVENT_STATUS_DONE, user_id=IDS["Users"][0]
    ),
    Events(
        id=IDS["Events"][0],
        title="title1",
        description="description1",
        due_date=datetime.datetime.utcnow(),
        user_id=IDS["Users"][0],
        type_id=IDS["Event_types"][0],
        status_id=IDS["Event_statuses"][1],
        hive_id=IDS["Hives"][0],
    ),
    Events(
        id=IDS["Events"][1],
        title="title2",
        description="description2",
        due_date=datetime.datetime.utcnow() + datetime.timedelta(days=1),
        user_id=IDS["Users"][0],
        type_id=IDS["Event_types"][1],
        status_id=IDS["Event_statuses"][0],
        hive_id=IDS["Hives"][0],
    ),
    CommentTypes(id=IDS["Comment_types"][0], name=COMMENT_TYPE_USER),
    CommentTypes(id=IDS["Comment_types"][1], name=COMMENT_TYPE_SYSTEM),
    Comments(
        id=uuid.uuid4(),
        comment="comment1",
        date=datetime.datetime.utcnow(),
        user_id=IDS["Users"][0],
        type_id=IDS["Comment_types"][0],
        swarm_id=IDS["Swarms"][0],
        hive_id=IDS["Hives"][0],
        apiary_id=IDS["Apiaries"][0],
    ),
    Comments(
        id=uuid.uuid4(),
        comment="comment2",
        date=datetime.datetime.utcnow(),
        user_id=IDS["Users"][0],
        type_id=IDS["Comment_types"][1],
        apiary_id=IDS["Apiaries"][2],
        event_id=IDS["Events"][0],
    ),
    Comments(
        id=uuid.uuid4(),
        comment="comment3",
        date=datetime.datetime.utcnow(),
        user_id=IDS["Users"][0],
        type_id=IDS["Comment_types"][0],
        swarm_id=IDS["Swarms"][1],
        hive_id=IDS["Hives"][1],
        apiary_id=IDS["Apiaries"][1],
    ),
    Comments(
        id=uuid.uuid4(),
        comment="comment4",
        date=datetime.datetime.utcnow(),
        user_id=IDS["Users"][0],
        type_id=IDS["Comment_types"][0],
        swarm_id=IDS["Swarms"][0],
        hive_id=IDS["Hives"][0],
        apiary_id=IDS["Apiaries"][0],
    ),
)