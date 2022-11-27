from uuid import UUID
import functools
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from akingbee.domains.aristaeus.commands.create_comment import CreateCommentCommand
from akingbee.domains.aristaeus.applications.comment import CommentApplication
from akingbee.domains.aristaeus.queries.comment import CommentQuery
from akingbee.domains.aristaeus.entities.comment import CommentEntity
from akingbee.domains.aristaeus.entities.user import UserEntity

from akingbee.controllers.api.aristaeus.dtos.comment import CommentIn
from akingbee.controllers.api.aristaeus.dtos.comment import CommentOut
from akingbee.controllers.api.aristaeus.utils.auth import auth_user

router = APIRouter()


@router.post("", response_model=CommentOut)
async def post_omment(input: CommentIn, user: UserEntity = Depends(auth_user)):
    command = CreateCommentCommand(
        hive_id=input.hive_id,
        event_id=input.hive_id,
        date=input.date,
        type=input.type,
        body=input.body,
    )
    comment_application = CommentApplication()
    comment_entity = await comment_application.create(command=command)

    return comment_entity.asdict()


@router.get("/{comment_id}", response_model=CommentOut)
async def get_omment(comment_id: UUID, user: UserEntity = Depends(auth_user)):
    omment_entity = await CommentQuery().get_comment_query(comment_id)
    return omment_entity.asdict()
