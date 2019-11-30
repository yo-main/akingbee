import datetime

from peewee import CharField, DateTimeField, TextField, ForeignKeyField
from .base import BaseModel
from .users import User
from .swarm import Swarm
from .apiary import Apiary
from .hive import Hive


class ActionType(BaseModel):
    fr = CharField()
    en = CharField()
    user = ForeignKeyField(User, backref="action_types")
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)


class StatusAction(BaseModel):
    fr = CharField()
    en = CharField()
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)


class Action(BaseModel):
    date = DateTimeField()
    user = ForeignKeyField(User, backref="actions")
    swarm = ForeignKeyField(Swarm, backref="actions", null=True)
    type = ForeignKeyField(ActionType, backref="actions")
    apiary = ForeignKeyField(Apiary, backref="actions", null=True)
    status = ForeignKeyField(StatusAction, backref="actions")
    hive = ForeignKeyField(Hive, backref="actions", null=True)
    deadline = DateTimeField(null=True)
    note = TextField()
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)
