import uuid

import pytest

from aristaeus.domain.entities.apiary import Apiary
from aristaeus.domain.entities.hive import Hive
from aristaeus.domain.entities.swarm import Swarm
from aristaeus.domain.errors import ApiaryCannotBeRemovedSwarmExists
from aristaeus.domain.errors import CantAttachSwarmNoApiary
from aristaeus.domain.errors import CantAttachSwarmOneAlreadyExists
from aristaeus.domain.errors import PermissionError


def test_hive_model():
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid.uuid4())

    assert hive.name == "name"
    assert hive.condition == "condition"
    assert hive.owner == "owner"
    assert hive.public_id is not None


def test_hive_change_owner():
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid.uuid4())
    hive.transfer_ownership("new")

    assert hive.owner == "new"


def test_hive_change_condition():
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid.uuid4())
    hive.update_condition("new")

    assert hive.condition == "new"


def test_hive_change_name():
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid.uuid4())
    hive.rename("new")

    assert hive.name == "new"


def test_hive_attach_swarm():
    apiary = Apiary(name="name", location="location", honey_kind="kind", organization_id=uuid.uuid4())
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid.uuid4(), apiary=apiary)
    swarm = Swarm(health="health", queen_year=1)

    assert hive.swarm is None

    hive.attach_swarm(swarm)

    assert hive.swarm.public_id == swarm.public_id


def test_hive_attach_swarm__no_apiary():
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid.uuid4())
    swarm = Swarm(health="health", queen_year=1)

    assert hive.swarm is None

    with pytest.raises(CantAttachSwarmNoApiary):
        hive.attach_swarm(swarm)


def test_hive_attach_swarm__already_exist():
    apiary = Apiary(name="name", location="location", honey_kind="kind", organization_id=uuid.uuid4())
    old_swarm = Swarm(health="health", queen_year=1)
    hive = Hive(
        name="name", condition="condition", owner="owner", organization_id=uuid.uuid4(), apiary=apiary, swarm=old_swarm
    )
    swarm = Swarm(health="health", queen_year=2)

    assert hive.swarm.public_id == old_swarm.public_id

    with pytest.raises(CantAttachSwarmOneAlreadyExists):
        hive.attach_swarm(swarm)


def test_hive_attach_swarm__idempotent():
    apiary = Apiary(name="name", location="location", honey_kind="kind", organization_id=uuid.uuid4())
    swarm = Swarm(health="health", queen_year=1)
    hive = Hive(
        name="name", condition="condition", owner="owner", organization_id=uuid.uuid4(), apiary=apiary, swarm=swarm
    )

    hive.attach_swarm(swarm)


def test_hive_move():
    apiary = Apiary(name="name", location="location", honey_kind="kind", organization_id=uuid.uuid4())
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=apiary.organization_id)

    assert hive.apiary is None

    hive.move(apiary)

    assert hive.apiary.public_id == apiary.public_id


def test_hive_move_different_organization():
    apiary = Apiary(name="name", location="location", honey_kind="kind", organization_id=uuid.uuid4())
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid.uuid4())

    assert hive.apiary is None

    with pytest.raises(PermissionError):
        hive.move(apiary)


def test_hive_remove():
    apiary = Apiary(name="name", location="location", honey_kind="kind", organization_id=uuid.uuid4())
    hive = Hive(
        name="name", condition="condition", owner="owner", organization_id=apiary.organization_id, apiary=apiary
    )

    assert hive.apiary is not None

    hive.remove_apiary()

    assert hive.apiary is None


def test_hive_remove_swarm():
    apiary = Apiary(name="name", location="location", honey_kind="kind", organization_id=uuid.uuid4())
    swarm = Swarm(health="health", queen_year=1)
    hive = Hive(
        name="name", condition="condition", owner="owner", organization_id=uuid.uuid4(), apiary=apiary, swarm=swarm
    )

    assert hive.apiary is not None

    with pytest.raises(ApiaryCannotBeRemovedSwarmExists):
        hive.remove_apiary()


def test_hive_remove__no_apiary():
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid.uuid4())

    assert hive.apiary is None

    hive.remove_apiary()

    assert hive.apiary is None
