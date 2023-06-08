from aristaeus.domain.entities.swarm import Swarm


def test_swarm_model():
    swarm = Swarm(health="health", queen_year=1)

    assert swarm.public_id is not None
    assert swarm.queen_year == 1
    assert swarm.health == "health"


def test_swarm_equal():
    swarm = Swarm(health="health", queen_year=1)
    other = Swarm(health="health", queen_year=1)

    assert swarm == swarm
    assert swarm != other


def test_swarm_change_year():
    swarm = Swarm(health="health", queen_year=1)
    assert swarm.queen_year == 1

    swarm.change_queen_year(2)
    assert swarm.queen_year == 2


def test_swarm_change_health():
    swarm = Swarm(health="health", queen_year=1)
    assert swarm.health == "health"

    swarm.change_health("new")
    assert swarm.health == "new"
