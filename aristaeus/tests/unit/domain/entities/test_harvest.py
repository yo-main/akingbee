import uuid
from datetime import date

import pytest

from aristaeus.domain.entities.harvest import Harvest
from aristaeus.domain.errors import CantHarvestNegativeQuantity


def test_harvest_model():
    harvest = Harvest(quantity=10, apiary_name="apiary_name", hive_id=uuid.uuid4(), date_harvest=date(2023, 1, 1))

    assert harvest.apiary_name == "apiary_name"
    assert harvest.quantity == 10
    assert harvest.date_harvest == date(2023, 1, 1)
    assert harvest.hive_id is not None


def test_harvest_equal():
    harvest1 = Harvest(quantity=100, apiary_name="apiary_name", hive_id=uuid.uuid4(), date_harvest=date(2023, 1, 1))
    harvest2 = Harvest(quantity=10, apiary_name="apiary_name", hive_id=harvest1.hive_id, date_harvest=date(2023, 1, 1))
    harvest3 = Harvest(quantity=1, apiary_name="apiary_name", hive_id=uuid.uuid4(), date_harvest=date(2023, 1, 1))
    harvest4 = Harvest(quantity=1, apiary_name="apiary_name", hive_id=harvest1.hive_id, date_harvest=date(2023, 2, 1))

    assert harvest1 == harvest2
    assert harvest1 != harvest3
    assert harvest1 != harvest4


def test_harvest__negative_quantity():
    with pytest.raises(CantHarvestNegativeQuantity):
        Harvest(quantity=-10, apiary_name="apiary_name", hive_id=uuid.uuid4(), date_harvest=date(2023, 1, 1))
