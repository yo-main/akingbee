import mysql.connector
import peewee as pw

from src.constants.environments import DATABASE
from src.constants.environments import PLATFORM_ENVIRONMENT

database = DATABASE[PLATFORM_ENVIRONMENT]

DB = pw.MySQLDatabase(**database)

# old class - to delete once refacto done
class MySQL:
    def __init__(self):
        self._create()

    def _create(self):
        self.conn = mysql.connector.connect(**database)
        return self.conn

    def cursor(self):
        return self.conn.cursor(buffered=True)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def rollback(self):
        self.conn.rollback()
