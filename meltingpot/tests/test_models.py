import sqlalchemy as sa

from meltingpot.database.utils.test import test_db
from meltingpot.models.base import Base

class TestModel(Base):
    __tablename__ = "testmodel"
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)

def test_models(test_db):
    meta = Base.metadata
    meta.create_all(test_db.engine)

    res = test_db.session.query(TestModel).all()
    assert len(res) == 0

    for _ in range(10):
        test_db.session.add(TestModel())
    test_db.session.commit()

    res = test_db.session.query(TestModel).all()
    assert len(res) == 10
