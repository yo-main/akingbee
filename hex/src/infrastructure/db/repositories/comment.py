import asyncio
import functools
from sqlalchemy import select

from domains.bee.entities.comment import CommentEntity
from domains.bee.errors import EntitySavingError
from infrastructure.db.models.comment import CommentModel
from infrastructure.db.repositories.base import BaseRepository
from domains.bee.entities.vo.reference import Reference


class CommentRepository(BaseRepository):
    async def get_async(self, reference: Reference) -> CommentEntity:
        query = select(CommentModel).where(CommentModel.public_id == reference.get())
        result = await self.database.execute_async(query)
        return result.scalar_one().to_entity()

    async def save_async(self, entity: CommentEntity) -> None:
        model = CommentModel.from_entity(entity)
        await self.database.save_async(model)
