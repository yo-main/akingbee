from peewee import MySQLDatabase, DatabaseProxy

from common.config import CONFIG
from common.log.logger import logger

DB = DatabaseProxy()


def init():
    # if not yet initialized
    if not DB.obj:
        database = MySQLDatabase(**CONFIG.DATABASE)
        logger.info("Initializing database...")
        DB.initialize(database)


