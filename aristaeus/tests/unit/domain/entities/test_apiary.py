from uuid import uuid4

from aristaeus.domain.entities.apiary import Apiary


def test_apiary_model():
    apiary = Apiary(name="name", location="location", honey_kind="honey_kind", organization_id=uuid4(), hive_count=1)

    assert apiary.name == "name"
    assert apiary.location == "location"
    assert apiary.honey_kind == "honey_kind"
    assert apiary.hive_count == 1
    assert apiary.public_id is not None


def test_apiary_equal():
    apiary = Apiary(name="name", location="location", honey_kind="honey_kind", organization_id=uuid4(), hive_count=1)
    other = Apiary(name="name", location="location", honey_kind="honey_kind", organization_id=uuid4(), hive_count=1)
    same = Apiary(
        name="name",
        location="location",
        honey_kind="honey_kind",
        organization_id=uuid4(),
        hive_count=1,
        public_id=apiary.public_id,
    )

    assert apiary != other
    assert apiary == same


def test_apiary_rename():
    apiary = Apiary(name="name", location="location", honey_kind="honey_kind", organization_id=uuid4(), hive_count=1)
    apiary.rename("new")

    assert apiary.name == "new"


def test_apiary_honey_kind():
    apiary = Apiary(name="name", location="location", honey_kind="honey_kind", organization_id=uuid4(), hive_count=1)
    apiary.change_honey_kind("new")

    assert apiary.honey_kind == "new"


def test_apiary_location():
    apiary = Apiary(name="name", location="location", honey_kind="honey_kind", organization_id=uuid4(), hive_count=1)
    apiary.change_location("new")

    assert apiary.location == "new"
