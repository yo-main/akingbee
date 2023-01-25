from uuid import UUID

from aristaeus.domain.entities.hive import DetailedHiveEntity
from aristaeus.domain.entities.hive import HiveEntity
from aristaeus.infrastructure.db.repositories.hive import HiveRepositoryAdapter
from aristaeus.injector import InjectorMixin


class HiveQuery(InjectorMixin):
    hive_repository: HiveRepositoryAdapter

    async def get_hive_query(self, hive_id: UUID) -> HiveEntity:
        return await self.hive_repository.get(hive_id)

    async def list_hives(self, organization_id: UUID) -> list[DetailedHiveEntity]:
        return await self.hive_repository.list(organization_id)
