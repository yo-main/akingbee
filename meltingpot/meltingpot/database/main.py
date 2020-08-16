import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from meltingpot.config import CONFIG
from meltingpot.helpers.metaclass import Box
from meltingpot.errors import AlreadyInitialized


def get_engine(url):
    echo_query = CONFIG.LOG_LEVEL <= logging.DEBUG
    engine = create_engine(url, echo=echo_query, pool_size=5, pool_recycle=3600)
    return engine

def get_database_url(dbname=None):
    user = CONFIG.DATABASE_USER
    pswd = CONFIG.DATABASE_PASSWORD
    host = CONFIG.DATABASE_HOST
    port = CONFIG.DATABASE_PORT
    dbnm = dbname or CONFIG.DATABASE_DATABASE

    if any(val is None for val in (user, pswd, host, port, dbnm)):
        raise ValueError("Database configuration is missing")

    return f"postgresql+psycopg2://{user}:{pswd}@{host}:{port}/{dbnm}"

class db:
    session = Box()
    engine = Box()
    url = None

    @classmethod
    def init(cls, url=None):
        url = url or get_database_url()

        if cls.url is not None:
            if cls.url == url:
                return
            raise AlreadyInitialized()

        cls.url = url

        self = cls()
        self.engine = get_engine(cls.url)
        self.session = scoped_session(sessionmaker(autoflush=False, bind=self.engine))

    @classmethod
    def clear(cls):
        cls.url = None
        self = cls()
        if self.session:
            self.session.remove()
            del self.session
        if self.engine:
            self.engine.dispose()
            del self.engine

    @classmethod
    def reset(cls):
        cls.clear()
        cls.init()

