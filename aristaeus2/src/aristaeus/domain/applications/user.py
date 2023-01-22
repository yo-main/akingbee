from typing import Any
from aristaeus.domain.adapters.repositories.user import UserRepositoryAdapter
from aristaeus.domain.adapters.repositories.parameter import ParameterRepositoryAdapter
from aristaeus.domain.commands.user import CreateUserCommand
from aristaeus.domain.entities.user import UserEntity
from aristaeus.injector import InjectorMixin
from aristaeus.domain.entities.parameter import ParameterEntity
from aristaeus.domain.entities.vo.hive_condition import HiveCondition
from aristaeus.domain.entities.vo.honey_type import HoneyType
from aristaeus.domain.entities.vo.swarm_health import SwarmHealth
from aristaeus.domain.entities.vo.event_type import EventType
from aristaeus.dispatcher import Dispatcher


class UserApplication(InjectorMixin):
    user_repository: UserRepositoryAdapter
    parameter_repository: ParameterRepositoryAdapter

    async def create(self, command: CreateUserCommand) -> UserEntity:
        user = UserEntity(
            public_id=command.public_id,
            organization_id=command.organization_id
        )

        await self.user_repository.save(user)
        Dispatcher.publish("user.created", user=user, language=command.language)
        return user

    async def initialize_user(self, user: UserEntity, language: str) -> None:
        print("Yay")
        parameters: list[Any] = HiveCondition.get_defaults(language)
        parameters.extend(HoneyType.get_defaults(language))
        parameters.extend(SwarmHealth.get_defaults(language))
        parameters.extend(EventType.get_defaults(language))

        for parameter in parameters:
            await self.parameter_repository.save(ParameterEntity.of(parameter, user.organization_id))
