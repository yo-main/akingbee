"""API endpoints for hive"""
import datetime
from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session

from gaea.log import logger
from gaea.models import Comments, Hives
from gaea.webapp.utils import get_session

from aristaeus.helpers.common import validate_uuid
from gaea.helpers.auth import get_logged_in_user
from aristaeus.models import CommentModel, PostCommentModel, PutCommentModel

router = APIRouter()


@router.get("/comments", status_code=200, response_model=List[CommentModel])
async def get_hive_comments(
    hive_id: Optional[uuid.UUID] = None,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Get a list of comments related to a hive
    """
    user_id = await get_logged_in_user(access_token)
    query = session.query(Comments).filter(
        Comments.user_id == user_id,
        Comments.deleted_at.is_(None),
    )

    if hive_id:
        hive = session.query(Hives).get(hive_id)
        if not hive or hive.user_id != user_id or hive.deleted_at:
            raise HTTPException(status_code=404)

        query = query.filter(Comments.hive_id == hive_id)

    return query.all()


@router.post("/comments/hive/{hive_id}", status_code=200, response_model=CommentModel)
async def post_hive_comments(
    hive_id: uuid.UUID,
    data: PostCommentModel,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Post a comment
    """
    user_id = await get_logged_in_user(access_token)
    hive = session.query(Hives).get(hive_id)
    if not hive or hive.user_id != user_id or hive.deleted_at:
        raise HTTPException(status_code=404)

    comment = Comments(
        user_id=user_id,
        hive_id=hive.id,
        swarm_id=hive.swarm_id,
        comment=data.comment,
        type="user",
        date=data.date,
        event_id=data.event_id,
    )

    session.add(comment)

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Database error", comment=comment)
        raise HTTPException(
            status_code=400, detail="Couldn't save the comment in database"
        ) from exc

    return comment


@router.put("/comments/{comment_id}", status_code=204)
async def put_comment(
    comment_id: uuid.UUID,
    data: PutCommentModel,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Modify a comment
    """
    user_id = await get_logged_in_user(access_token)
    comment = session.query(Comments).get(comment_id)
    if not comment or comment.user_id != user_id or comment.deleted_at:
        raise HTTPException(status_code=404)

    for key, value in data.dict().items():
        if value is not None:
            setattr(comment, key, value)

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Database error", comment=comment)
        raise HTTPException(
            status_code=400, detail="Couldn't update the comment in database"
        ) from exc


@router.delete("/comments/{comment_id}", status_code=204)
async def del_comment(
    comment_id: uuid.UUID,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """
    Delete a comment
    """
    user_id = await get_logged_in_user(access_token)
    comment = session.query(Comments).get(comment_id)
    if not comment or comment.user_id != user_id or comment.deleted_at:
        raise HTTPException(status_code=404)

    comment.deleted_at = datetime.datetime.now()

    try:
        session.commit()
    except Exception as exc:
        logger.exception("Database error", comment=comment)
        raise HTTPException(
            status_code=400, detail="Couldn't mark a comment as deleted in database"
        ) from exc
