from peewee import MySQLDatabase, SqliteDatabase, DatabaseProxy

from common.config import CONFIG

DB = DatabaseProxy()


def init():
    if CONFIG.ENV == "TEST":
        database = SqliteDatabase(":memory:", pragmas=(("foreign_keys", 1),))
    else:
        database = MySQLDatabase(**CONFIG.DATABASE)

    DB.initialize(database)

    if CONFIG.ENV == "TEST":
        from common.models import MODELS, User

        DB.create_tables(MODELS)
