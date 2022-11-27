from uuid import UUID
import functools
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from akingbee.domains.aristaeus.commands.create_apiary import CreateApiaryCommand
from akingbee.domains.aristaeus.applications.apiary import ApiaryApplication
from akingbee.domains.aristaeus.queries.apiary import ApiaryQuery
from akingbee.domains.aristaeus.entities.apiary import ApiaryEntity
from akingbee.domains.aristaeus.entities.user import UserEntity

from akingbee.controllers.api.aristaeus.dtos.apiary import ApiaryIn
from akingbee.controllers.api.aristaeus.dtos.apiary import ApiaryOut
from akingbee.controllers.api.aristaeus.utils.auth import auth_user

router = APIRouter()


@router.post("", response_model=ApiaryOut)
async def post_apiary(input: ApiaryIn, user: UserEntity = Depends(auth_user)):
    command = CreateApiaryCommand(
        name=input.name, location=input.location, honey_kind=input.honey_kind, organization_id=user.organization_id
    )
    apiary_application = ApiaryApplication()
    apiary_entity = await apiary_application.create(command=command)

    return apiary_entity.asdict()


@router.get("/{apiary_id}", response_model=ApiaryOut)
async def get_apiary(apiary_id: UUID, user: UserEntity = Depends(auth_user)):
    apiary_entity = await ApiaryQuery().get_apiary_query(apiary_id)
    return apiary_entity.asdict()
