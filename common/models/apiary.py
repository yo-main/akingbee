import datetime

from peewee import CharField, DateTimeField, ForeignKeyField, DateField

from .base import BaseModel
from .users import User


class StatusApiary(BaseModel):
    fr = CharField()
    en = CharField()
    user = ForeignKeyField(User, backref="apiary_statuses")
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)


class HoneyType(BaseModel):
    fr = CharField()
    en = CharField()
    user = ForeignKeyField(User, backref="honey_types")
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)


class Apiary(BaseModel):
    user = ForeignKeyField(User, backref="apiaries")
    name = CharField()
    status = ForeignKeyField(StatusApiary, backref="apiaries")
    birthday = DateField()
    location = CharField()
    honey_type = ForeignKeyField(HoneyType, backref="apiaries")
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)
