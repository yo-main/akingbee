from uuid import UUID

from fastapi import APIRouter, Depends

from akingbee.controllers.api.aristaeus.dtos.apiary import ApiaryIn, ApiaryOut
from akingbee.controllers.api.aristaeus.utils.auth import auth_user
from akingbee.domains.aristaeus.applications.apiary import ApiaryApplication
from akingbee.domains.aristaeus.commands.create_apiary import CreateApiaryCommand
from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.domains.aristaeus.queries.apiary import ApiaryQuery

router = APIRouter()


@router.post("", response_model=ApiaryOut)
async def post_apiary(input: ApiaryIn, user: UserEntity = Depends(auth_user)):
    command = CreateApiaryCommand(
        name=input.name, location=input.location, honey_kind=input.honey_kind, organization_id=user.organization_id
    )
    apiary_application = ApiaryApplication()
    apiary_entity = await apiary_application.create(command=command)

    return apiary_entity.asdict()


@router.get("", response_model=list[ApiaryOut])
async def list_apiary(user: UserEntity = Depends(auth_user)):
    apiary_entities = await ApiaryQuery().list_apiary_query(user.organization_id)
    return [apiary.asdict() for apiary in apiary_entities]


@router.get("/{apiary_id}", response_model=ApiaryOut)
async def get_apiary(apiary_id: UUID, user: UserEntity = Depends(auth_user)):
    apiary_entity = await ApiaryQuery().get_apiary_query(apiary_id)
    return apiary_entity.asdict()
