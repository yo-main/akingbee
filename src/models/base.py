import flask
from peewee import Model

from src.database import DB
from src.errors import errors


class BaseModel(Model):
    class Meta:
        database = DB

        # allow 'smart' name for table (with the use of _)
        legacy_table_names = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columns = [
            field.column.name for field in self.alias().get_field_aliases()
        ]

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
                raise errors.UserCouldNotBeIdentified()

    def serialize(self):
        data = {column: getattr(self, column) for column in self.columns}
        return data
