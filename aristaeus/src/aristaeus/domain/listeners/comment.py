from datetime import datetime

from aristaeus.dispatcher import Dispatcher
from aristaeus.domain.commands.comment import CreateCommentCommand
from aristaeus.domain.entities.hive import Hive
from aristaeus.domain.entities.user import User
from aristaeus.domain.services.comment import CommentApplication

TRANSLATIONS = {
    "hive.created": {"fr": "Ruche créée", "en": "Hive created"},
    "hive.moved": {"fr": "Ruche déménagée vers la ruche {name}", "en": "Hive moved to apiary {name}"},
    "hive.removed": {"fr": "Ruche mise en stock", "en": "Hive put in storage"},
}


@Dispatcher.subscribe("hive.created")
async def on_hive_created(hive: Hive, requester: User):
    service = CommentApplication()
    command = CreateCommentCommand(
        hive_id=hive.public_id,
        type="system",
        date=datetime.now(),
        body=TRANSLATIONS["hive.created"][requester.language],
    )
    await service.create(command)


@Dispatcher.subscribe("hive.moved")
async def on_hive_moved(hive: Hive, requester: User):
    service = CommentApplication()
    command = CreateCommentCommand(
        hive_id=hive.public_id,
        type="system",
        date=datetime.now(),
        body=TRANSLATIONS["hive.moved"][requester.language].format(name=hive.apiary.name),
    )
    await service.create(command)


@Dispatcher.subscribe("hive.removed")
async def on_hive_removed(hive: Hive, requester: User):
    service = CommentApplication()
    command = CreateCommentCommand(
        hive_id=hive.public_id,
        type="system",
        date=datetime.now(),
        body=TRANSLATIONS["hive.removed"][requester.language],
    )
    await service.create(command)
