import asyncio
import functools
from uuid import UUID

from sqlalchemy import select

from akingbee.domains.aristaeus.adapters.repositories.comment import (
    CommentRepositoryAdapter,
)
from akingbee.domains.aristaeus.entities.comment import CommentEntity
from akingbee.domains.aristaeus.errors import EntitySavingError
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.models.comment import CommentModel
from akingbee.infrastructure.db.utils import error_handler
from akingbee.injector import Injector


@Injector.bind(CommentRepositoryAdapter)
class CommentRepository:
    database: AsyncDatabase

    @error_handler
    async def get(self, comment_id: UUID) -> CommentEntity:
        query = select(CommentModel).where(CommentModel.public_id == comment_id)
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    @error_handler
    async def save(self, entity: CommentEntity) -> None:
        model = CommentModel.from_entity(entity)
        await self.database.save(model, commit=True)
