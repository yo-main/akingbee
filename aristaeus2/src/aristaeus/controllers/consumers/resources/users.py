import logging

import uuid

from aristaeus.domain.applications.user import UserApplication
from aristaeus.domain.commands.user import CreateUserCommand

logger = logging.getLogger(__name__)


async def on_user_created(properties, body):
    user_id = body["user"]["id"]
    organization_id = str(uuid.uuid4())
    language = body["language"]

    user_application = UserApplication()
    await user_application.create(command=CreateUserCommand(
        public_id=user_id,
        organization_id=organization_id,
        language=language,
    ))

    logger.info("User %s initialized", user_id)
