from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from meltingpot.config import CONFIG


def get_engine():
    url = get_database_url()
    if url is None:
        raise ValueError("Database configuration is missing")

    engine = create_engine(url)
    return engine

def get_database_url():
    user = CONFIG.DATABASE_USER
    pswd = CONFIG.DATABASE_PASSWORD
    host = CONFIG.DATABASE_HOST
    port = CONFIG.DATABASE_PORT
    dbnm = CONFIG.DATABASE_DATABASE

    if any(val is None for val in (user, pswd, host, port, dbnm)):
        return None

    return f"postgresql+psycopg2://{user}:{pswd}@{host}:{port}/{dbnm}"

session_factory = sessionmaker(bind=get_engine())

Session = scoped_session(session_factory)
