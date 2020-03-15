import datetime

from peewee import CharField, DateTimeField, DateField, ForeignKeyField

from .base import BaseModel
from .users import User, Owner
from .swarm import Swarm
from .apiary import Apiary


class HiveCondition(BaseModel):
    fr = CharField()
    en = CharField()
    user = ForeignKeyField(User, backref="hive_statuses")
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)


class Hive(BaseModel):
    user = ForeignKeyField(User, backref="hives")
    name = CharField()
    owner = ForeignKeyField(Owner, backref="hives")
    apiary = ForeignKeyField(Apiary, backref="hives")
    swarm = ForeignKeyField(Swarm, backref="hives", null=True)
    condition = ForeignKeyField(HiveCondition, backref="hives")
    birthday = DateField()
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)
