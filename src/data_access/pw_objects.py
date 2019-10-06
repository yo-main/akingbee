import datetime

import flask
import peewee as pw

from src.services.logger import logger
from src.data_access.connectors import DB
from src.services.alerts import Error
from src.constants import alert_codes as alerts


class BaseModel(pw.Model):
    class Meta:
        database = DB

        # allow 'smart' name for table (with the use of _)
        legacy_table_names = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columns = [field.column.name
                        for field in self.alias().get_field_aliases()]

        # logger.info("USER {}: {} {} object with columns \n{}"
        #             .format(flask.session["user_id"],
        #                     self.__class__.__name__,
        #                     self.id,
        #                     self.columns))

        # make sure that we automatically attach the current user_id to any object
        # it's probably buggy, to refactor - TODO
        if "user_id" in self.columns and self.user_id is None:
            self._create_user_id(kwargs.get("user_id"))


    def _create_user_id(self, user_id_kwargs):
        """
        Add the user id to the newly created object
        we look in the flask session objects first
        and check in the kwargs provided in case we haven't found it
        an error is raised if no user id is found anywhere
        """
        try:
            setattr(self, "user_id", flask.session["user_id"])
        except KeyError:
            if user_id_kwargs:
                setattr(self, "user_id", user_id_kwargs)
            else:
                raise Error(alerts.USER_COULD_NOT_BE_IDENTIFIED)


    def serialize(self):
        data = {column: getattr(self, column)
                for column in self.columns}
        return data




class User(BaseModel):
    username =              pw.CharField(unique=True)
    pwd =                   pw.CharField()
    email =                 pw.CharField()
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)
    date_last_connection =  pw.DateTimeField(null=True)


class ActionType(BaseModel):
    fr =                    pw.CharField()
    en =                    pw.CharField()
    user =                  pw.ForeignKeyField(User, backref="action_types")
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)


class CommentType(BaseModel):
    fr =                    pw.CharField()
    en =                    pw.CharField()
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)


class HiveCondition(BaseModel):
    fr =                    pw.CharField()
    en =                    pw.CharField()
    user =                  pw.ForeignKeyField(User, backref="hive_statuses")
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)


class SwarmHealth(BaseModel):
    fr =                    pw.CharField()
    en =                    pw.CharField()
    user =                  pw.ForeignKeyField(User, backref="swarm_healths")
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)


class HoneyType(BaseModel):
    fr =                    pw.CharField()
    en =                    pw.CharField()
    user =                  pw.ForeignKeyField(User, backref="honey_types")
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)


class Owner(BaseModel):
    name =                  pw.CharField()
    user =                  pw.ForeignKeyField(User, backref="owners")
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)


class StatusAction(BaseModel):
    fr =                    pw.CharField()
    en =                    pw.CharField()
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)


class StatusApiary(BaseModel):
    fr =                    pw.CharField()
    en =                    pw.CharField()
    user =                  pw.ForeignKeyField(User, backref="apiary_statuses")
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)



class Apiary(BaseModel):
    user =                  pw.ForeignKeyField(User, backref="apiaries")
    name =                  pw.CharField()
    status =                pw.ForeignKeyField(StatusApiary, backref="apiaries")
    birthday =              pw.DateField()
    location =              pw.CharField()
    honey_type =            pw.ForeignKeyField(HoneyType, backref="apiaries")
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)


class Swarm(BaseModel):
    user =                  pw.ForeignKeyField(User, backref="swarms")
    health =                pw.ForeignKeyField(SwarmHealth, backref="swarms")
    birthday =              pw.DateField()
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)


class Hive(BaseModel):
    user =                  pw.ForeignKeyField(User, backref="hives")
    name =                  pw.CharField()
    owner =                 pw.ForeignKeyField(Owner, backref="hives")
    apiary =                pw.ForeignKeyField(Apiary, backref="hives")
    swarm =                 pw.ForeignKeyField(Swarm, backref="hives", null=True)
    condition =             pw.ForeignKeyField(HiveCondition, backref="hives")
    birthday =              pw.DateField()
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)


class Action(BaseModel):
    date =                  pw.DateTimeField()
    user =                  pw.ForeignKeyField(User, backref="actions")
    swarm =                 pw.ForeignKeyField(Swarm, backref="actions", null=True)
    type =                  pw.ForeignKeyField(ActionType, backref="actions")
    apiary =                pw.ForeignKeyField(Apiary, backref="actions", null=True)
    status =                pw.ForeignKeyField(StatusAction, backref="actions")
    hive =                  pw.ForeignKeyField(Hive, backref="actions", null=True)
    deadline =              pw.DateTimeField()
    description =           pw.TextField()
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)


class Comment(BaseModel):
    date =                  pw.DateTimeField()
    user =                  pw.ForeignKeyField(User, backref="comments")
    swarm =                 pw.ForeignKeyField(Swarm, backref="comments", null=True)
    type =                  pw.ForeignKeyField(CommentType, backref="comments")
    apiary =                pw.ForeignKeyField(Apiary, backref="comments", null=True)
    health =                pw.ForeignKeyField(SwarmHealth, backref="comments", null=True)
    action =                pw.ForeignKeyField(Action, backref="comments", null=True)
    comment =               pw.TextField()
    hive =                  pw.ForeignKeyField(Hive, backref="comments", null=True)
    date_creation =         pw.DateTimeField(default=datetime.datetime.now)
    date_modification =     pw.DateTimeField(default=datetime.datetime.now)




MODELS = (
    User,
    ActionType,
    CommentType,
    HiveCondition,
    SwarmHealth,
    HoneyType,
    Owner,
    StatusAction,
    StatusApiary,
    Apiary,
    Hive,
    Swarm,
    Action,
    Comment
)






