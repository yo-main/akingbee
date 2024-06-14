from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from aristaeus.controllers.api.dtos.apiary import ApiaryOut
from aristaeus.controllers.api.dtos.apiary import DetailedApiaryOut
from aristaeus.controllers.api.dtos.apiary import PostApiaryIn
from aristaeus.controllers.api.dtos.apiary import PutApiaryIn
from aristaeus.controllers.api.utils.auth import auth_user
from aristaeus.domain.services.apiary import ApiaryService
from aristaeus.domain.commands.apiary import CreateApiaryCommand
from aristaeus.domain.commands.apiary import PutApiaryCommand
from aristaeus.domain.entities.user import User
from aristaeus.domain.queries.apiary import ApiaryQuery

router = APIRouter()


@router.post("", response_model=ApiaryOut, status_code=201)
async def post_apiary(input: PostApiaryIn, user: User = Depends(auth_user)):
    command = CreateApiaryCommand(
        name=input.name, location=input.location, honey_kind=input.honey_kind, organization_id=user.organization_id
    )
    apiary_service = ApiaryService()
    apiary_entity = await apiary_service.create(command=command)

    return apiary_entity.asdict()


@router.get("", response_model=list[DetailedApiaryOut])
async def list_apiary(user: User = Depends(auth_user)):
    apiary_entities = await ApiaryQuery().list_apiary_query(user.organization_id)
    return [apiary.asdict() for apiary in apiary_entities]


@router.get("/{apiary_id}", response_model=ApiaryOut)
async def get_apiary(apiary_id: UUID, user: User = Depends(auth_user)):
    apiary_entity = await ApiaryQuery().get_apiary_query(apiary_id)
    return apiary_entity.asdict()


@router.put("/{apiary_id}", response_model=ApiaryOut)
async def put_apiary(apiary_id: UUID, input: PutApiaryIn, user: User = Depends(auth_user)):
    command = PutApiaryCommand(
        name=input.name, location=input.location, honey_kind=input.honey_kind, apiary_id=apiary_id
    )
    apiary_service = ApiaryService()
    apiary_entity = await apiary_service.put(command=command)
    return apiary_entity.asdict()


@router.delete("/{apiary_id}", status_code=204)
async def delete_apiary(apiary_id: UUID, user: User = Depends(auth_user)):
    apiary_service = ApiaryService()
    await apiary_service.delete(apiary_id=apiary_id)
    return 204
