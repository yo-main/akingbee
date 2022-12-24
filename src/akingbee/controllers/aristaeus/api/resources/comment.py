from uuid import UUID

from fastapi import APIRouter, Depends

from akingbee.controllers.aristaeus.api.dtos.comment import (
    CommentOut,
    PostCommentIn,
    PutCommentIn,
)
from akingbee.controllers.aristaeus.api.utils.auth import auth_user
from akingbee.domains.aristaeus.applications.comment import CommentApplication
from akingbee.domains.aristaeus.commands.comment import (
    CreateCommentCommand,
    PutCommentCommand,
)
from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.domains.aristaeus.queries.comment import CommentQuery

router = APIRouter()


@router.post("", response_model=CommentOut)
async def post_comment(input: PostCommentIn, user: UserEntity = Depends(auth_user)):
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
async def get_comment(comment_id: UUID, user: UserEntity = Depends(auth_user)):
    omment_entity = await CommentQuery().get_comment_query(comment_id)
    return omment_entity.asdict()


@router.get("", response_model=list[CommentOut])
async def list_comment(hive_id: UUID, user: UserEntity = Depends(auth_user)):
    comments = await CommentQuery().list_comment_query(hive_id)
    return [comment.asdict() for comment in comments]


@router.put("/{comment_id}", response_model=CommentOut)
async def put_comment(comment_id: UUID, input: PutCommentIn, user: UserEntity = Depends(auth_user)):
    command = PutCommentCommand(comment_id=comment_id, date=input.date, type=input.type, body=input.body)
    comment_application = CommentApplication()
    comment_entity = await comment_application.put(command=command)
    return comment_entity.asdict()


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(comment_id: UUID, user: UserEntity = Depends(auth_user)):
    comment_application = CommentApplication()
    await comment_application.delete(comment_id=comment_id)
    return 204
