from uuid import UUID

from aristaeus.domain.entities.apiary import Apiary
from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.injector import InjectorMixin


class ApiaryQuery(InjectorMixin):
    async def get_apiary_query(self, apiary_id: UUID) -> Apiary:
        async with UnitOfWork() as uow:
            return await uow.apiary.get(apiary_id)

    async def list_apiary_query(self, organization_id: UUID) -> list[Apiary]:
        async with UnitOfWork() as uow:
            return await uow.apiary.list(organization_id)
