import contextlib
import uuid

import pytest

from meltingpot.database.main import db, get_database_url
from meltingpot.models.base import Base


@contextlib.contextmanager
def get_temporary_database():
    db_client = db()
    session = db_client.get_session()
    conn = session.connection()

    dbname = "test_" + str(uuid.uuid4()).replace("-", "")
    conn.execute("commit")
    conn.execute(f"CREATE DATABASE {dbname}")
    conn.execute("commit")

    yield dbname

    conn.execute(
        f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
        f"WHERE datname = '{dbname}'"
    )
    conn.execute(f"DROP DATABASE {dbname}")
    conn.execute("commit")


@pytest.fixture(scope="module", autouse=True)
def test_db_url():
    with get_temporary_database() as dbname:
        url = get_database_url(dbname)
        db_client = db(url=url)

        Base.metadata.create_all(db_client.engine)

        db_client.clear()

        yield url
