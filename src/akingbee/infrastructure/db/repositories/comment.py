import asyncio
import functools
from sqlalchemy import select

from domains.bee.entities.comment import CommentEntity
from domains.bee.errors import EntitySavingError
from domains.bee.adapters.repository.comment import CommentRepositoryAdapter
from infrastructure.db.models.comment import CommentModel
from infrastructure.db.engine import AsyncDatabase
from domains.bee.entities.vo.reference import Reference
from injector import Injector


@Injector.bind(CommentRepositoryAdapter)
class CommentRepository:
    database: AsyncDatabase

    async def get_async(self, reference: Reference) -> CommentEntity:
        query = select(CommentModel).where(CommentModel.public_id == reference.get())
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    async def save_async(self, entity: CommentEntity) -> None:
        model = CommentModel.from_entity(entity)
        await self.database.save(model)
