import pytest

from gaea.database import db
from gaea.database.utils.test import get_temporary_database


@pytest.fixture(scope="module")
def test_db():
    with get_temporary_database() as db_url:
        db_client = db(url=db_url)
        yield db_client
        db_client.clear()