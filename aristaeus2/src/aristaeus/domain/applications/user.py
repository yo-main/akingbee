from aristaeus.domain.adapters.repositories.user import UserRepositoryAdapter
from aristaeus.domain.adapters.repositories.parameter import ParameterRepositoryAdapter
from aristaeus.domain.commands.user import CreateUserCommand
from aristaeus.domain.entities.user import UserEntity
from aristaeus.injector import InjectorMixin


class UserApplication(InjectorMixin):
    user_repository: UserRepositoryAdapter
    parameter_repository: ParameterRepositoryAdapter

    async def create(self, command: CreateUserCommand) -> UserEntity:

        user = UserEntity(
            public_id=command.public_id,
            organization_id=command.organization_id
        )

        await self.user_repository.save(user)
        return user
