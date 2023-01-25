import asyncio
import functools
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from aristaeus.domain.adapters.repositories.comment import CommentRepositoryAdapter
from aristaeus.domain.entities.comment import CommentEntity
from aristaeus.infrastructure.db.engine import AsyncDatabase
from aristaeus.infrastructure.db.models.comment import CommentModel
from aristaeus.infrastructure.db.models.event import EventModel
from aristaeus.infrastructure.db.models.hive import HiveModel
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.infrastructure.db.utils import get_data_from_entity
from aristaeus.injector import Injector


@Injector.bind(CommentRepositoryAdapter)
class CommentRepository:
    database: AsyncDatabase

    @error_handler
    async def get(self, comment_id: UUID) -> CommentEntity:
        query = select(CommentModel).where(CommentModel.public_id == comment_id)
        result = await self.database.execute(query)
        return result.unique().scalar_one().to_entity()

    @error_handler
    async def save(self, comment: CommentEntity) -> None:
        data = get_data_from_entity(comment)

        if "hive_id" in data:
            sub_query = select(HiveModel.id).where(HiveModel.public_id == data["hive_id"])
            data["hive_id"] = sub_query

        if "event_id" in data:
            sub_query = select(EventModel.id).where(EventModel.public_id == data["event_id"])
            data["event_id"] = sub_query

        query = insert(CommentModel).values(data)
        await self.database.execute(query)

    @error_handler
    async def update(self, comment: CommentEntity, fields: list[str]) -> CommentEntity:
        query = (
            update(CommentModel)
            .values({field: getattr(comment, field) for field in fields})
            .where(CommentModel.public_id == comment.public_id)
        )
        await self.database.execute(query)
        return await self.get(comment.public_id)

    @error_handler
    async def delete(self, comment: CommentEntity) -> None:
        query = delete(CommentModel).where(CommentModel.public_id == comment.public_id)
        await self.database.execute(query)

    @error_handler
    async def list(self, hive_id: UUID) -> list[CommentEntity]:
        query = (
            select(CommentModel)
            .join(HiveModel, HiveModel.id == CommentModel.hive_id)
            .where(HiveModel.public_id == hive_id)
        )
        result = await self.database.execute(query)
        return [model.to_entity() for model in result.unique().scalars()]
