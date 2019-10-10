from peewee import MySQLDatabase
from playhouse.sqlite_ext import SqliteExtDatabase

from src.constants.environments import DATABASE
from src.constants.environments import PLATFORM_ENVIRONMENT

if PLATFORM_ENVIRONMENT == "DEV":
    DB = SqliteExtDatabase(":memory:", pragmas=(
        ("foreign_keys", 1),
    ))
    
    from src.data_access.pw_objects import MODELS
    DB.create_tables(MODELS)
else:
    database = DATABASE[PLATFORM_ENVIRONMENT]
    DB = MySQLDatabase(**database)
