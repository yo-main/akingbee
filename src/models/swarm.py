import datetime

from peewee import CharField, DateTimeField, DateField, ForeignKeyField

from .base import BaseModel
from .users import User


class SwarmHealth(BaseModel):
    fr = CharField()
    en = CharField()
    user = ForeignKeyField(User, backref="swarm_healths")
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)


class Swarm(BaseModel):
    user = ForeignKeyField(User, backref="swarms")
    health = ForeignKeyField(SwarmHealth, backref="swarms")
    birthday = DateField()
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)
