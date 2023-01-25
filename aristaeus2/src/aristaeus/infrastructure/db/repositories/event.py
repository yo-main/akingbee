from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from aristaeus.domain.adapters.repositories.event import EventRepositoryAdapter
from aristaeus.domain.entities.event import EventEntity
from aristaeus.infrastructure.db.engine import AsyncDatabase
from aristaeus.infrastructure.db.models.event import EventModel
from aristaeus.infrastructure.db.models.hive import HiveModel
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.infrastructure.db.utils import get_data_from_entity
from aristaeus.injector import Injector


@Injector.bind(EventRepositoryAdapter)
class EventRepository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> EventEntity:
        query = select(EventModel).where(EventModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.unique().scalar_one().to_entity()

    @error_handler
    async def save(self, event: EventEntity) -> None:
        data = get_data_from_entity(event)

        if "hive_id" in data:
            sub_query = select(HiveModel.id).where(HiveModel.public_id == data["hive_id"])
            data["hive_id"] = sub_query

        query = insert(EventModel).values(data)
        await self.database.execute(query)

    @error_handler
    async def update(self, event: EventEntity, fields: list[str]) -> EventEntity:
        query = (
            update(EventModel)
            .values({field: getattr(event, field) for field in fields})
            .where(EventModel.public_id == event.public_id)
        )
        await self.database.execute(query)
        return await self.get(event.public_id)

    @error_handler
    async def delete(self, event: EventEntity) -> None:
        query = delete(EventModel).where(EventModel.public_id == event.public_id)
        await self.database.execute(query)

    @error_handler
    async def list(self, hive_id: UUID) -> list[EventEntity]:
        query = (
            select(EventModel).join(HiveModel, HiveModel.id == EventModel.hive_id).where(HiveModel.public_id == hive_id)
        )
        result = await self.database.execute(query)
        return [model.to_entity() for model in result.unique().scalars()]
