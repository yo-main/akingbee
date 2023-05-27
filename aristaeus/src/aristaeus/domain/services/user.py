from typing import Any
from uuid import UUID

from aristaeus.dispatcher import Dispatcher
from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.domain.commands.user import CreateUserCommand
from aristaeus.domain.entities.parameter import Parameter
from aristaeus.domain.entities.user import User
from aristaeus.domain.entities.vo.event_type import EventType
from aristaeus.domain.entities.vo.hive_condition import HiveCondition
from aristaeus.domain.entities.vo.honey_kind import HoneyKind
from aristaeus.domain.entities.vo.owner import Owner
from aristaeus.domain.entities.vo.swarm_health import SwarmHealth
from aristaeus.injector import InjectorMixin


class UserApplication(InjectorMixin):
    async def create(self, command: CreateUserCommand) -> User:
        user = User(public_id=command.public_id, organization_id=command.organization_id)

        async with UnitOfWork() as uow:
            await uow.user.save(user)
            await uow.commit()

        Dispatcher.publish(
            "user.created", user_public_id=user.public_id, language=command.language, username=command.username
        )
        return user

    async def initialize_user(self, user_public_id: UUID, language: str, username: str) -> None:
        async with UnitOfWork() as uow:
            user = await uow.user.get(public_id=user_public_id)

            parameters: list[Any] = HiveCondition.get_defaults(language)
            parameters.extend(HoneyKind.get_defaults(language))
            parameters.extend(SwarmHealth.get_defaults(language))
            parameters.extend(EventType.get_defaults(language))
            parameters.append(Owner(value=username))

            for parameter in parameters:
                await uow.parameter.save(Parameter.of(parameter, user.organization_id))

            await uow.commit()
