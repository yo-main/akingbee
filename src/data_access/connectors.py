import sqlite3
import mysql.connector

from src.constants.config import DATABASE, ENVIRONMENT


database = DATABASE[ENVIRONMENT['platform']]


class MySQL:
    def __enter__(self):
        self.conn = mysql.connector.connect(**database)
        return self.conn.cursor(buffered=True)

    def __exit__(self, type_, value, error):
        self.conn.commit()
        self.conn.close()


class SQLite:
    def __enter__(self):
        self.conn = sqlite3.connect('database.db')
        return self.conn.cursor()

    def __exit__(self, type_, value, error):
        self.conn.commit()
        self.conn.close()

