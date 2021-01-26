"""API endpoints for hive"""
import datetime
from typing import List
import uuid

from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session

from gaea.log import logger
from gaea.models import Comments, Hives
from gaea.webapp.utils import get_session

from aristaeus.helpers.common import validate_uuid
from aristaeus.helpers.authentication import get_logged_in_user
from aristaeus.models import CommentModel

router = APIRouter()

@router.get("/hive/{hive_id}/comments", status_code=200, response_model=List[CommentModel])
async def get_hive_comments(hive_id: uuid.UUID, access_token: str = Cookie(None), session: Session = Depends(get_session)):
    """
    Get a list of comments related to a hive
    """
    user_id = await get_logged_in_user(access_token)
    hive = session.query(Hives).get(hive_id)
    if not hive or hive.user_id != user_id or hive.deleted_at:
        raise HTTPException(status_code=404)

    comments = session.query(Comments).filter(Comments.user_id == user_id, Comments.deleted_at.is_(None), Comments.hive_id == hive_id).all()
    return comments
