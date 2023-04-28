from typing import Any
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from aristaeus.domain.adapters.repositories.comment import CommentRepositoryAdapter
from aristaeus.domain.entities.comment import CommentEntity
from aristaeus.domain.errors import EntityNotFound
from aristaeus.infrastructure.db.engine import AsyncDatabase
from aristaeus.infrastructure.db import orm
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.injector import Injector


@Injector.bind(CommentRepositoryAdapter, "test")
class FakeCommentRepository:
    _comments: set[CommentEntity] = set()

    @error_handler
    async def get(self, public_id: UUID) -> CommentEntity:
        try:
            return next(comment for comment in self._comments if comment.public_id == public_id)
        except StopIteration:
            raise EntityNotFound("Comment not found")

    @error_handler
    async def save(self, comment: CommentEntity) -> None:
        self._comments.add(comment)

    @error_handler
    async def update(self, comment: CommentEntity) -> None:
        self._comments.discard(comment)
        self._comments.add(comment)

    @error_handler
    async def list(self, hive_id: UUID) -> list[CommentEntity]:
        return [comment for comment in self._comments if comment.hive.public_id == hive_id]

    @error_handler
    async def delete(self, comment: CommentEntity) -> None:
        self._comments.discard(comment)


@Injector.bind(CommentRepositoryAdapter)
class CommentRepository:
    database: AsyncDatabase

    @error_handler
    async def get(self, comment_id: UUID) -> CommentEntity:
        query = (
            select(CommentEntity)
            .join_from(orm.comment_table, orm.hive_table)
            .join_from(orm.comment_table, orm.event_table, isouter=True)
            .where(orm.comment_table.c.public_id == comment_id)
        )
        result = await self.database.execute(query)
        return result.unique().scalar_one()

    @error_handler
    async def save(self, comment: CommentEntity) -> None:
        data = {
            "date": comment.date,
            "type": comment.type,
            "body": comment.body,
            "public_id": comment.public_id,
            "hive_id": select(orm.hive_table.c.id).where(orm.hive_table.c.public_id == comment.hive.public_id),
        }

        if comment.event_id:
            data["event_id"] = select(orm.event_table.c.id).where(orm.event_table.c.public_id == comment.event.public_id)

        query = insert(orm.comment_table).values(data)
        await self.database.execute(query)

    @error_handler
    async def update(self, comment: CommentEntity) -> None:
        data: dict[Any, Any] = {"date": comment.date, "body": comment.body}
        query = update(orm.comment_table).values(data).where(orm.comment_table.c.public_id == comment.public_id)
        await self.database.execute(query)

    @error_handler
    async def delete(self, comment: CommentEntity) -> None:
        query = delete(orm.comment_table).where(orm.comment_table.c.public_id == comment.public_id)
        await self.database.execute(query)

    @error_handler
    async def list(self, hive_id: UUID) -> list[CommentEntity]:
        query = select(CommentEntity).join_from(orm.comment_table, orm.hive_table).where(orm.hive_table.c.public_id == hive_id)
        result = await self.database.execute(query)
        return result.unique().scalars().all()
