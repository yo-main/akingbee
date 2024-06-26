from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from aristaeus.controllers.api.dtos.comment import CommentOut
from aristaeus.controllers.api.dtos.comment import PostCommentIn
from aristaeus.controllers.api.dtos.comment import PutCommentIn
from aristaeus.controllers.api.utils.auth import auth_user
from aristaeus.domain.services.comment import CommentApplication
from aristaeus.domain.commands.comment import CreateCommentCommand
from aristaeus.domain.commands.comment import PutCommentCommand
from aristaeus.domain.entities.user import User
from aristaeus.domain.queries.comment import CommentQuery

router = APIRouter()


@router.post("/{hive_id}", response_model=CommentOut)
async def post_comment(hive_id: UUID, input: PostCommentIn, user: User = Depends(auth_user)):
    command = CreateCommentCommand(
        hive_id=hive_id,
        event_id=input.event_id,
        date=input.date,
        type="user",
        body=input.body,
    )
    comment_application = CommentApplication()
    comment_entity = await comment_application.create(command=command)

    return comment_entity.asdict()


@router.get("/{comment_id}", response_model=CommentOut)
async def get_comment(comment_id: UUID, user: User = Depends(auth_user)):
    comment_entity = await CommentQuery().get_comment_query(comment_id)
    return comment_entity.asdict()


@router.get("", response_model=list[CommentOut])
async def list_comment(hive_id: UUID, user: User = Depends(auth_user)):
    comments = await CommentQuery().list_comment_query(hive_id)
    comments.sort(key=lambda c: c.date, reverse=True)
    return [comment.asdict() for comment in comments]


@router.put("/{comment_id}", response_model=CommentOut)
async def put_comment(comment_id: UUID, input: PutCommentIn, user: User = Depends(auth_user)):
    command = PutCommentCommand(comment_id=comment_id, date=input.date, body=input.body)
    comment_application = CommentApplication()
    comment_entity = await comment_application.put(command=command)
    return comment_entity.asdict()


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(comment_id: UUID, user: User = Depends(auth_user)):
    comment_application = CommentApplication()
    await comment_application.delete(comment_id=comment_id)
    return 204
