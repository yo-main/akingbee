from peewee import MySQLDatabase, SqliteDatabase, DatabaseProxy

from src.constants.environments import DATABASE
from src.constants.environments import PLATFORM_ENVIRONMENT

DB = DatabaseProxy()


def init():
    if PLATFORM_ENVIRONMENT == "TEST":
        database = SqliteDatabase(":memory:", pragmas=(("foreign_keys", 1),))
    else:
        database = MySQLDatabase(**DATABASE[PLATFORM_ENVIRONMENT])

    DB.initialize(database)

    if PLATFORM_ENVIRONMENT == "TEST":
        from src.models import MODELS

        DB.create_tables(MODELS)
