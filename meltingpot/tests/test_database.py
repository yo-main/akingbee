import pytest

from meltingpot.errors import AlreadyInitialized, NotInitialized

from meltingpot.database import db

def test_db_client():
    with pytest.raises(NotInitialized):
        assert db.session

    db.init(url="sqlite://")

    old_session = db.session
    db.session.execute("SELECT 1")
    db.session.commit()

    db.init(url="sqlite://")

    assert db.session is old_session

    with pytest.raises(AlreadyInitialized):
        db.init(url="sqlite:///")

    db.clear()
    with pytest.raises(NotInitialized):
        assert db.session

    db.init()
    assert db.session is not old_session

    db.clear()
