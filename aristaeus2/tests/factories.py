import uuid

import factory

from aristaeus.infrastructure.db.models.apiary import ApiaryModel
from aristaeus.infrastructure.db.models.comment import CommentModel
from aristaeus.infrastructure.db.models.event import EventModel
from aristaeus.infrastructure.db.models.hive import HiveModel
from aristaeus.infrastructure.db.models.parameter import ParameterModel


class HiveModelFactory(factory.Factory):
    class Meta:
        model = HiveModel

    public_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    condition = factory.Faker("word")
    owner = factory.Faker("word")
    organization_id = factory.LazyFunction(uuid.uuid4)


class ApiaryModelFactory(factory.Factory):
    class Meta:
        model = ApiaryModel

    public_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    location = factory.Faker("word")
    honey_kind = factory.Faker("word")
    organization_id = factory.LazyFunction(uuid.uuid4)


class CommentModelFactory(factory.Factory):
    class Meta:
        model = CommentModel

    public_id = factory.LazyFunction(uuid.uuid4)
    hive_id = factory.LazyFunction(uuid.uuid4)
    body = factory.Faker("word")
    type = factory.Faker("word")
    date = factory.Faker("date_time")


class EventModelFactory(factory.Factory):
    class Meta:
        model = EventModel

    public_id = factory.LazyFunction(uuid.uuid4)
    hive_id = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker("word")
    description = factory.Faker("word")
    status = factory.Faker("word")
    type = factory.Faker("word")
    due_date = factory.Faker("date_time")


class ParameterModelFactory(factory.Factory):
    class Meta:
        model = ParameterModel

    public_id = factory.LazyFunction(uuid.uuid4)
    key = factory.Faker("word")
    value = factory.Faker("word")
    organization_id = factory.LazyFunction(uuid.uuid4)
