from .base import BaseModel
from .users import User, Owner
from .swarm import SwarmHealth, Swarm
from .apiary import StatusApiary, HoneyType, Apiary
from .hive import HiveCondition, Hive
from .events import EventType, StatusEvent, Event
from .comment import CommentType, Comment

MODELS = (
    User,
    Owner,
    SwarmHealth,
    Swarm,
    StatusApiary,
    HoneyType,
    Apiary,
    HiveCondition,
    Hive,
    EventType,
    StatusEvent,
    Event,
    CommentType,
    Comment,
)
