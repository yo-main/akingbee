import datetime

from peewee import CharField, DateTimeField, ForeignKeyField

from .base import BaseModel

class User(BaseModel):
    username = CharField(unique=True)
    pwd = CharField()
    email = CharField()
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)
    date_last_connection = DateTimeField(null=True)


class Owner(BaseModel):
    name = CharField()
    user = ForeignKeyField(User, backref="owners")
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)