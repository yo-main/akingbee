from .base import BaseModel
from .users import User, Owner
from .swarm import SwarmHealth, Swarm
from .apiary import StatusApiary, HoneyType, Apiary
from .hive import HiveCondition, Hive
from .action import ActionType, StatusAction, Action
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
    ActionType,
    StatusAction,
    Action,
    CommentType,
    Comment
)
