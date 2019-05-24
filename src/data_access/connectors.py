import mysql.connector

from src.constants.config import DATABASE
from src.constants.environments import PLATFORM_ENVIRONMENT

database = DATABASE[PLATFORM_ENVIRONMENT]


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
