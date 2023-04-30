from uuid import UUID

from aristaeus.domain.entities.hive import Hive
from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.injector import InjectorMixin


class HiveQuery(InjectorMixin):
    async def get_hive_query(self, hive_id: UUID) -> Hive:
        async with UnitOfWork() as uow:
            return await uow.hive.get(hive_id)

    async def list_hives(self, organization_id: UUID) -> list[Hive]:
        async with UnitOfWork() as uow:
            return await uow.hive.list(organization_id)
