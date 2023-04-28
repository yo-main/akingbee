from typing import Any
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert

from aristaeus.domain.adapters.repositories.parameter import ParameterRepositoryAdapter
from aristaeus.domain.entities.parameter import Parameter
from aristaeus.domain.errors import EntityNotFound
from aristaeus.infrastructure.db.engine import AsyncDatabase
from aristaeus.infrastructure.db import orm
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.injector import Injector


@Injector.bind(ParameterRepositoryAdapter, "test")
class FakeParameterRepository:
    _parameters: set[Parameter] = set()

    @error_handler
    async def get(self, public_id: UUID) -> Parameter:
        try:
            return next(parameter for parameter in self._parameters if parameter.public_id == public_id)
        except StopIteration:
            raise EntityNotFound("Parameter not found")

    @error_handler
    async def save(self, parameter: Parameter) -> None:
        self._parameters.add(parameter)

    @error_handler
    async def update(self, parameter: Parameter) -> None:
        self._parameters.discard(parameter)
        self._parameters.add(parameter)

    @error_handler
    async def list(self, organization_id: UUID, key: str | None = None) -> list[Parameter]:
        return [
            parameter
            for parameter in self._parameters
            if parameter.organization_id == organization_id and (parameter.key == key if key else True)
        ]

    @error_handler
    async def delete(self, parameter: Parameter) -> None:
        self._parameters.discard(parameter)


@Injector.bind(ParameterRepositoryAdapter)
class ParameterRespository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> Parameter:
        query = select(Parameter).where(orm.parameter_table.c.public_id == public_id)
        result = await self.database.execute(query)
        return result.scalar_one()

    @error_handler
    async def save(self, parameter: Parameter) -> None:
        data = {
            "key": parameter.key,
            "value": parameter.value,
            "public_id": parameter.public_id,
            "organization_id": parameter.organization_id,
        }
        query = insert(orm.parameter_table).values(data).on_conflict_do_nothing()
        await self.database.execute(query)

    @error_handler
    async def update(self, parameter: Parameter) -> None:
        data: dict[Any, Any] = {"value": parameter.value}
        query = update(orm.parameter_table).values(data).where(orm.parameter_table.c.public_id == parameter.public_id)
        await self.database.execute(query)

    @error_handler
    async def delete(self, parameter: Parameter) -> None:
        query = delete(orm.parameter_table).where(orm.parameter_table.c.public_id == parameter.public_id)
        await self.database.execute(query)

    @error_handler
    async def list(self, organization_id: UUID, key: str | None = None) -> list[Parameter]:
        query = select(Parameter).where(orm.parameter_table.c.organization_id == organization_id)
        if key is not None:
            query = query.where(orm.parameter_table.c.key == key)
        result = await self.database.execute(query)
        return result.unique().scalars().all()
