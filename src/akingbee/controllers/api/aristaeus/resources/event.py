import functools
from uuid import UUID

from akingbee.controllers.api.aristaeus.dtos.event import EventIn, EventOut
from akingbee.controllers.api.aristaeus.utils.auth import auth_user
from akingbee.domains.aristaeus.applications.event import EventApplication
from akingbee.domains.aristaeus.commands.create_event import CreateEventCommand
from akingbee.domains.aristaeus.entities.event import EventEntity
from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.domains.aristaeus.queries.event import EventQuery
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("", response_model=EventOut)
async def post_event(input: EventIn, user: UUID = Depends(auth_user)):
    command = CreateEventCommand(
        title=input.title,
        description=input.description,
        type=input.type,
        status=input.status,
        due_date=input.due_date,
        hive_id=input.hive_id,
    )
    event_application = EventApplication()
    event_entity = await event_application.create(command=command)

    return event_entity.asdict()


@router.get("/{event_id}", response_model=EventOut)
async def get_event(event_id: UUID, user: UserEntity = Depends(auth_user)):
    event_entity = await EventQuery().get_event_query(event_id)
    return event_entity.asdict()
