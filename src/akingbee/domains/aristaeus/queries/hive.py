from uuid import UUID

from akingbee.domains.aristaeus.entities.hive import HiveEntity
from akingbee.infrastructure.db.repositories.hive import HiveRepositoryAdapter
from akingbee.injector import InjectorMixin


class HiveQuery(InjectorMixin):
    hive_repository: HiveRepositoryAdapter

    async def get_hive_query(self, hive_id: UUID) -> HiveEntity:
        return await self.hive_repository.get(hive_id)
