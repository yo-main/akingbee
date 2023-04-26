from uuid import UUID

from aristaeus.domain.entities.apiary import ApiaryEntity
from aristaeus.infrastructure.db.repositories.apiary import ApiaryRepositoryAdapter
from aristaeus.injector import InjectorMixin


class ApiaryQuery(InjectorMixin):
    apiary_repository: ApiaryRepositoryAdapter

    async def get_apiary_query(self, apiary_id: UUID) -> ApiaryEntity:
        return await self.apiary_repository.get(apiary_id)

    async def list_apiary_query(self, organization_id: UUID) -> list[ApiaryEntity]:
        return await self.apiary_repository.list(organization_id)
