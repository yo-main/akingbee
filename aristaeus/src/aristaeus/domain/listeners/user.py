from uuid import UUID

from aristaeus.dispatcher import Dispatcher
from aristaeus.domain.services.user import UserApplication


@Dispatcher.subscribe("user.created")
async def on_user_created(user_public_id: UUID, language: str, username: str):
    user_application = UserApplication()
    await user_application.initialize_user(user_public_id=user_public_id, language=language, username=username)
