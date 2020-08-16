import pytest

from meltingpot.database import db



@pytest.fixture(scope="session")
def test_db():
    db.init(url="sqlite://")
    return db
