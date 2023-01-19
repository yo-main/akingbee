from aristaeus.dispatcher import Dispatcher
from aristaeus.domain.applications.user import UserApplication
from aristaeus.domain.entities.user import UserEntity


@Dispatcher.subscribe("user.created")
async def on_user_created(user: UserEntity, language: str):
    user_application = UserApplication()
    await user_application.initialize_user(user=user, language=language)
