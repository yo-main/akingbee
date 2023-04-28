import uuid

import factory

from aristaeus.domain.entities.apiary import ApiaryEntity
from aristaeus.domain.entities.hive import HiveEntity
from aristaeus.domain.entities.comment import CommentEntity
from aristaeus.domain.entities.event import EventEntity
from aristaeus.domain.entities.parameter import ParameterEntity
from aristaeus.domain.entities.swarm import SwarmEntity


class HiveEntityFactory(factory.Factory):
    class Meta:
        model = HiveEntity

    public_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    condition = factory.Faker("word")
    owner = factory.Faker("word")
    organization_id = factory.LazyFunction(uuid.uuid4)


class ApiaryEntityFactory(factory.Factory):
    class Meta:
        model = ApiaryEntity

    public_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    location = factory.Faker("word")
    honey_kind = factory.Faker("word")
    organization_id = factory.LazyFunction(uuid.uuid4)


class CommentEntityFactory(factory.Factory):
    class Meta:
        model = CommentEntity

    public_id = factory.LazyFunction(uuid.uuid4)
    hive = factory.SubFactory(HiveEntityFactory)
    body = factory.Faker("word")
    type = factory.Faker("word")
    date = factory.Faker("date_time")


class EventEntityFactory(factory.Factory):
    class Meta:
        model = EventEntity

    public_id = factory.LazyFunction(uuid.uuid4)
    hive = factory.SubFactory(HiveEntityFactory)
    title = factory.Faker("word")
    description = factory.Faker("word")
    status = factory.Faker("word")
    type = factory.Faker("word")
    due_date = factory.Faker("date_time")


class ParameterEntityFactory(factory.Factory):
    class Meta:
        model = ParameterEntity

    public_id = factory.LazyFunction(uuid.uuid4)
    key = factory.Faker("word")
    value = factory.Faker("word")
    organization_id = factory.LazyFunction(uuid.uuid4)


class SwarmEntityFactory(factory.Factory):
    class Meta:
        model = SwarmEntity

    public_id = factory.LazyFunction(uuid.uuid4)
    health = factory.Faker("word")
    queen_year = factory.Faker("random_int")
