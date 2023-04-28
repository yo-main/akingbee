import uuid

import factory

from aristaeus.domain.entities.apiary import Apiary
from aristaeus.domain.entities.hive import Hive
from aristaeus.domain.entities.comment import Comment
from aristaeus.domain.entities.event import Event
from aristaeus.domain.entities.parameter import Parameter
from aristaeus.domain.entities.swarm import Swarm


class HiveFactory(factory.Factory):
    class Meta:
        model = Hive

    public_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    condition = factory.Faker("word")
    owner = factory.Faker("word")
    organization_id = factory.LazyFunction(uuid.uuid4)


class ApiaryFactory(factory.Factory):
    class Meta:
        model = Apiary

    public_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    location = factory.Faker("word")
    honey_kind = factory.Faker("word")
    organization_id = factory.LazyFunction(uuid.uuid4)


class CommentFactory(factory.Factory):
    class Meta:
        model = Comment

    public_id = factory.LazyFunction(uuid.uuid4)
    hive = factory.SubFactory(HiveFactory)
    body = factory.Faker("word")
    type = factory.Faker("word")
    date = factory.Faker("date_time")


class EventFactory(factory.Factory):
    class Meta:
        model = Event

    public_id = factory.LazyFunction(uuid.uuid4)
    hive = factory.SubFactory(HiveFactory)
    title = factory.Faker("word")
    description = factory.Faker("word")
    status = factory.Faker("word")
    type = factory.Faker("word")
    due_date = factory.Faker("date_time")


class ParameterFactory(factory.Factory):
    class Meta:
        model = Parameter

    public_id = factory.LazyFunction(uuid.uuid4)
    key = factory.Faker("word")
    value = factory.Faker("word")
    organization_id = factory.LazyFunction(uuid.uuid4)


class SwarmFactory(factory.Factory):
    class Meta:
        model = Swarm

    public_id = factory.LazyFunction(uuid.uuid4)
    health = factory.Faker("word")
    queen_year = factory.Faker("random_int")
