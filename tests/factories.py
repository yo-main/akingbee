import uuid

import factory

from akingbee.infrastructure.db.models.apiary import ApiaryModel
from akingbee.infrastructure.db.models.comment import CommentModel
from akingbee.infrastructure.db.models.hive import HiveModel


class HiveModelFactory(factory.Factory):
    class Meta:
        model = HiveModel

    public_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    condition = factory.Faker("word")
    owner_id = factory.LazyFunction(uuid.uuid4)
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
