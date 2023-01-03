from uuid import UUID

from fastapi import APIRouter, Depends

from aristaeus.controllers.api.dtos.event import (
    EventOut,
    PostEventIn,
    PutEventIn,
)
from aristaeus.controllers.api.utils.auth import auth_user
from aristaeus.domain.applications.event import EventApplication
from aristaeus.domain.commands.event import (
    CreateEventCommand,
    PutEventCommand,
)
from aristaeus.domain.entities.user import UserEntity
from aristaeus.domain.queries.event import EventQuery

router = APIRouter()


@router.post("", response_model=EventOut)
async def post_event(input: PostEventIn, user: UUID = Depends(auth_user)):
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


@router.get("", response_model=list[EventOut])
async def list_event(hive_id: UUID, user: UserEntity = Depends(auth_user)):
    events = await EventQuery().list_event_query(hive_id)
    return [event.asdict() for event in events]


@router.put("/{event_id}", response_model=EventOut)
async def put_event(event_id: UUID, input: PutEventIn, user: UserEntity = Depends(auth_user)):
    command = PutEventCommand(
        event_id=event_id,
        due_date=input.due_date,
        status=input.status,
        title=input.title,
        description=input.description,
    )
    event_application = EventApplication()
    event_entity = await event_application.put(command=command)
    return event_entity.asdict()


@router.delete("/{event_id}", status_code=204)
async def delete_event(event_id: UUID, user: UserEntity = Depends(auth_user)):
    event_application = EventApplication()
    await event_application.delete(event_id=event_id)
    return 204
