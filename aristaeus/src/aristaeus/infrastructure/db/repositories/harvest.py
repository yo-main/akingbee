from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from aristaeus.domain.adapters.repositories.harvest import HarvestRepositoryAdapter
from aristaeus.domain.entities.harvest import Harvest
from aristaeus.infrastructure.db import orm
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.injector import Injector

from .base import BaseRepository


@Injector.bind(HarvestRepositoryAdapter, "test")
class FakeHarvestRepository(BaseRepository):
    _harvests: set[Harvest] = set()

    def __init__(self, session):
        self.session = session

    async def list(self, hive_id: UUID) -> list[Harvest]:
        return [harvest for harvest in self._harvests if harvest.hive_id == hive_id]

    async def save(self, harvest: Harvest) -> None:
        if harvest not in self._harvests:
            self._harvests.add(harvest)


@Injector.bind(HarvestRepositoryAdapter)
class HarvestRepository(BaseRepository):
    @error_handler
    async def get(self, hive_id: UUID) -> Harvest:
        query = select(Harvest).where(orm.harvest_table.c.hive_id == hive_id)
        result = await self.session.execute(query)
        objs = result.scalars()
        return objs

    @error_handler
    async def save(self, harvest: Harvest) -> None:
        data = {
            "hive_id": harvest.hive_id,
            "quantity": harvest.quantity,
            "date_harvest": harvest.date_harvest,
            "apiary_name": harvest.apiary_name,
        }
        query = insert(orm.harvest_table).values(data).on_conflict_do_nothing()

        await self.session.execute(query)
