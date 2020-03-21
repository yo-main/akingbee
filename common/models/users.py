import datetime

from peewee import CharField, DateTimeField, ForeignKeyField, UUIDField

from .base import BaseModel


class User(BaseModel):
    username = CharField(unique=True)
    pwd = CharField()
    email = CharField(unique=True)
    reset_pwd_id = UUIDField(null=True)
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)
    date_last_connection = DateTimeField(null=True)


class Owner(BaseModel):
    name = CharField()
    user = ForeignKeyField(User, backref="owners")
    date_creation = DateTimeField(default=datetime.datetime.now)
    date_modification = DateTimeField(default=datetime.datetime.now)
