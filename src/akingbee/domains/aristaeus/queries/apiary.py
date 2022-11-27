from uuid import UUID
from akingbee.domains.aristaeus.entities.apiary import ApiaryEntity
from akingbee.infrastructure.db.repositories.apiary import ApiaryRepositoryAdapter

from akingbee.injector import InjectorMixin


class ApiaryQuery(InjectorMixin):
    apiary_repository: ApiaryRepositoryAdapter

    async def get_apiary_query(self, apiary_id: UUID) -> ApiaryEntity:
        return await self.apiary_repository.get(apiary_id)
