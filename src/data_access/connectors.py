import sqlite3
import mysql.connector

from src.constants.config import DATABASE, ENVIRONMENT


database = DATABASE[ENVIRONMENT['platform']]


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


class SQLite:
    def __enter__(self):
        self.conn = sqlite3.connect('database.db')
        return self.conn.cursor()

    def __exit__(self, type_, value, error):
        self.conn.commit()
        self.conn.close()

