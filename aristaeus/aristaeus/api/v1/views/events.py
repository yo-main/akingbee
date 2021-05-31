"""API endpoints for events"""

import datetime
from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session

from gaea.log import logger
from gaea.models import Events, Hives
from gaea.webapp.utils import get_session

from aristaeus.helpers.common import validate_uuid
from aristaeus.helpers.authentication import get_logged_in_user
from aristaeus.models import EventModel, PostEventModel, PutEventModel

router = APIRouter()


@router.get("/events", status_code=200, response_model=List[EventModel])
async def get_events(
    hive_id: Optional[uuid.UUID] = None,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Get a list of events
    """
    user_id = await get_logged_in_user(access_token)
    query = session.query(Events).filter(Events.user_id == user_id)
    if hive_id:
        query = query.filter(Events.hive_id == hive_id)

    return query.all()


@router.get("/events/{event_id}", status_code=200, response_model=EventModel)
async def get_event(
    event_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Get a single event
    """
    user_id = await get_logged_in_user(access_token)
    event = session.query(Events).get(event_id)
    if not event or event.user_id != user_id or event.deleted_at:
        raise HTTPException(status_code=404)

    return event


@router.post("/events", status_code=200, response_model=EventModel)
async def post_event(
    data: PostEventModel,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Post an event
    """
    user_id = await get_logged_in_user(access_token)

    if data.hive_id:
        hive = session.query(Hives).get(data.hive_id)
        if not hive or hive.user_id != user_id or hive.deleted_at:
            raise HTTPException(status_code=404)

    event = Events(
        user_id=user_id,
        hive_id=data.hive_id,
        due_date=data.due_date,
        type_id=data.type_id,
        status_id=data.status_id,
        title=data.title,
        description=data.description,
    )

    session.add(event)

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Database error", event=event)
        raise HTTPException(
            status_code=400, detail="Couldn't save the comment in database"
        ) from exc

    return event


@router.put("/events/{event_id}", status_code=204)
async def put_event(
    event_id: uuid.UUID,
    data: PutEventModel,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Modify an event
    """
    user_id = await get_logged_in_user(access_token)
    event = session.query(Events).get(event_id)
    if not event or event.user_id != user_id or event.deleted_at:
        raise HTTPException(status_code=404)

    for key, value in data.dict().items():
        if value is not None:
            setattr(event, key, value)

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Database error", event=event)
        raise HTTPException(
            status_code=400, detail="Couldn't update the event in database"
        ) from exc


@router.delete("/events/{event_id}", status_code=204)
async def del_event(
    event_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Delete an event
    """
    user_id = await get_logged_in_user(access_token)
    event = session.query(Events).get(event_id)
    if not event or event.user_id != user_id or event.deleted_at:
        raise HTTPException(status_code=404)

    event.deleted_at = datetime.datetime.now()

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Database error", event=event)
        raise HTTPException(
            status_code=400, detail="Couldn't mark a event as deleted in database"
        ) from exc
