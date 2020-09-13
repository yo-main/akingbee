import pytest

from gaea.errors import AlreadyInitialized, NotInitialized

from gaea.database import db

def test_db_client():
    db_client = db(url="sqlite://")

    session = db_client.get_session()
    session.execute("SELECT 1").fetchall()
    session.commit()

    with db_client as new_session:
        assert session != new_session

    session.close()
    db_client.clear()
