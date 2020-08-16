import contextlib
import uuid

import pytest

from meltingpot.database.main import db, get_database_url
from meltingpot.models.base import Base


@contextlib.contextmanager
def get_temporary_database():
    db.init()
    master_conn = db.session.connection()

    dbname = "test_" + str(uuid.uuid4()).replace("-", "")
    master_conn.execute("commit")
    master_conn.execute(f"CREATE DATABASE {dbname}")

    db.clear()

    yield dbname

    db.clear()

    db.init()
    master_conn = db.session.connection()

    master_conn.execute("commit")
    master_conn.execute(f"DROP DATABASE {dbname}")


@pytest.fixture(scope="module")
def test_db():
    with get_temporary_database() as dbname:
        url = get_database_url(dbname)
        db.init(url)

        Base.metadata.create_all(db.engine)

        yield db
