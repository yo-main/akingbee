import pytest

from gaea.models import Hives, Apiaries, Swarms
from gaea.models.base import Base
from gaea.models.utils.test import DATASETS, IDS

from tests.fixtures import test_db


def test_models(test_db):
    meta = Base.metadata
    meta.create_all(test_db.engine)

    with test_db as session:
        for dataset in DATASETS:
            session.bulk_save_objects(dataset)
            session.commit()

    with test_db as session:
        hives = session.query(Hives).all()

        assert len(hives) == len(IDS["Hives"])

        hive = hives[0]
        assert hive.user.id == IDS["Users"][0]
        assert hive.apiary.id == IDS["Apiaries"][0]
        assert hive.swarm.id == IDS["Swarms"][0]

        swarm = session.query(Swarms).get(IDS["Swarms"][0])
        assert swarm.hive.id == hive.id

        apiary = session.query(Apiaries).get(IDS["Apiaries"][0])
        assert apiary.hives[0].id == hive.id
        assert apiary.nb_hives == 1

        with pytest.raises(IndexError):
            assert apiary.hives[1]