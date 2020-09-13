import sqlalchemy as sa

from tests.fixtures import test_db
from gaea.models.base import Base

class TestModel(Base):
    __tablename__ = "testmodel"
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)

def test_models(test_db):
    with test_db as session:
        meta = Base.metadata
        meta.create_all(test_db.engine)

        res = session.query(TestModel).all()
        assert len(res) == 0

        for _ in range(10):
            session.add(TestModel())
        session.commit()

        res = session.query(TestModel).all()
        assert len(res) == 10
