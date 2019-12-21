import datetime

from peewee import CharField, DateTimeField, TextField, ForeignKeyField
from .base import BaseModel
from .users import User
from .swarm import Swarm
from .apiary import Apiary
from .hive import Hive


class EventType(BaseModel):
    fr = CharField()
    en = CharField()
    user = ForeignKeyField(User, backref="event_types")
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)


class StatusEvent(BaseModel):
    fr = CharField()
    en = CharField()
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)


class Event(BaseModel):
    date = DateTimeField()
    user = ForeignKeyField(User, backref="events")
    swarm = ForeignKeyField(Swarm, backref="events", null=True)
    type = ForeignKeyField(EventType, backref="events")
    apiary = ForeignKeyField(Apiary, backref="events", null=True)
    status = ForeignKeyField(StatusEvent, backref="events")
    hive = ForeignKeyField(Hive, backref="events", null=True)
    deadline = DateTimeField(null=True)
    note = TextField()
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)
