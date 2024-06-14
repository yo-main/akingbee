from typing import Any
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from aristaeus.domain.adapters.repositories.hive import HiveRepositoryAdapter
from aristaeus.domain.entities.hive import Hive
from aristaeus.domain.errors import EntityNotFound
from aristaeus.infrastructure.db import orm
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.injector import Injector

from .base import BaseRepository


@Injector.bind(HiveRepositoryAdapter, "test")
class FakeHiveRepository(BaseRepository):
    _hives: set[Hive] = set()

    async def get(self, public_id: UUID) -> Hive:
        try:
            return next(hive for hive in self._hives if hive.public_id == public_id)
        except StopIteration:
            raise EntityNotFound("Hive not found")

    async def get_from_swarm_id(self, public_id: UUID) -> Hive:
        try:
            return next(hive for hive in self._hives if hive.swarm and hive.swarm.public_id == public_id)
        except StopIteration:
            raise EntityNotFound("Hive not found")

    async def save(self, hive: Hive) -> None:
        self._hives.add(hive)

    async def update(self, hive: Hive) -> None:
        self._hives.discard(hive)
        self._hives.add(hive)

    async def list(self, organization_id: UUID, with_apiary_only: bool | None) -> list[Hive]:
        return [
            hive
            for hive in self._hives
            if hive.organization_id == organization_id
            if (
                with_apiary_only is None
                or (hive.apiary is not None and with_apiary_only is True)
                or (hive.apiary is None and with_apiary_only is False)
            )
        ]

    async def delete(self, hive: Hive) -> None:
        self._hives.discard(hive)


@Injector.bind(HiveRepositoryAdapter)
class HiveRepository(BaseRepository):
    @error_handler()
    async def get(self, public_id: UUID) -> Hive:
        query = (
            select(Hive)
            .join_from(orm.hive_table, orm.apiary_table, isouter=True)
            .join_from(orm.hive_table, orm.swarm_table, isouter=True)
            .where(orm.hive_table.c.public_id == public_id)
        )
        result = await self.session.execute(query)
        return result.unique().scalar_one()

    @error_handler()
    async def get_from_swarm_id(self, public_id: UUID) -> Hive:
        query = (
            select(Hive)
            .join_from(orm.hive_table, orm.apiary_table, isouter=True)
            .join_from(orm.hive_table, orm.swarm_table, isouter=True)
            .where(orm.swarm_table.c.public_id == public_id)
        )
        result = await self.session.execute(query)
        return result.unique().scalar_one()

    def _get_relation_queries(self, hive: Hive) -> dict:
        data = {}
        apiary_id = hive.apiary.public_id if hive.apiary else None
        swarm_id = hive.swarm.public_id if hive.swarm else None

        if apiary_id:
            sub_query = select(orm.apiary_table.c.id).where(orm.apiary_table.c.public_id == apiary_id).scalar_subquery()
            data["apiary_id"] = sub_query
        else:
            data["apiary_id"] = None

        if swarm_id:
            sub_query = select(orm.swarm_table.c.id).where(orm.swarm_table.c.public_id == swarm_id).scalar_subquery()
            data["swarm_id"] = sub_query
        else:
            data["swarm_id"] = None

        return data

    @error_handler()
    async def save(self, hive: Hive) -> None:
        data: dict[Any, Any] = {
            "name": hive.name,
            "condition": hive.condition,
            "owner": hive.owner,
            "public_id": hive.public_id,
            "organization_id": hive.organization_id,
        }
        data.update(self._get_relation_queries(hive))

        query = insert(orm.hive_table).values(data)
        await self.session.execute(query)

    @error_handler()
    async def update(self, hive: Hive) -> None:
        data: dict[Any, Any] = {
            "name": hive.name,
            "condition": hive.condition,
            "owner": hive.owner,
        }
        data.update(self._get_relation_queries(hive))
        query = update(orm.hive_table).values(data).where(orm.hive_table.c.public_id == hive.public_id)
        await self.session.execute(query)

    @error_handler()
    async def delete(self, hive: Hive) -> None:
        query = delete(orm.hive_table).where(orm.hive_table.c.public_id == hive.public_id)
        await self.session.execute(query)

    @error_handler()
    async def list(self, organization_id: UUID, with_apiary_only: bool | None) -> list[Hive]:
        query = (
            select(Hive)
            .join_from(orm.hive_table, orm.apiary_table, isouter=True)
            .join_from(orm.hive_table, orm.swarm_table, isouter=True)
            .where(orm.hive_table.c.organization_id == organization_id)
        )

        if with_apiary_only is True:
            query = query.where(orm.hive_table.c.apiary_id.isnot(None))
        elif with_apiary_only is False:
            query = query.where(orm.hive_table.c.apiary_id.is_(None))

        result = await self.session.execute(query)
        return result.unique().scalars().all()
