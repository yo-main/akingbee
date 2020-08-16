import sqlalchemy as sa

from meltingpot.models.base import Base

from tests.fixtures import test_db


class TestModel(Base):
    __tablename__ = "testmodel"
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)

def test_models(test_db):
    meta = Base.metadata
    meta.create_all(test_db.engine)

    test_db.session.query(TestModel).all()
    assert len(test_db) == 0

    for _ in range(10):
        test_db.session.add(TestModel())
    test_db.session.commit()

    test_db.session.query(TestModel).all()
    assert len(test_db) == 10
