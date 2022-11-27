import functools
from uuid import UUID

from akingbee.controllers.api.aristaeus.dtos.parameter import ParameterIn, ParameterOut
from akingbee.controllers.api.aristaeus.utils.auth import auth_user
from akingbee.domains.aristaeus.applications.parameter import ParameterApplication
from akingbee.domains.aristaeus.commands.create_parameter import CreateParameterCommand
from akingbee.domains.aristaeus.entities.parameter import ParameterEntity
from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.domains.aristaeus.queries.parameter import ParameterQuery
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("", response_model=ParameterOut)
async def post_parameter(input: ParameterIn, user: UserEntity = Depends(auth_user)):
    command = CreateParameterCommand(key=input.key, value=input.value, organization_id=user.organization_id)
    parameter_application = ParameterApplication()
    parameter_entity = await parameter_application.create(command=command)

    return parameter_entity.asdict()


@router.get("/{parameter_id}", response_model=ParameterOut)
async def get_parameter(parameter_id: UUID, user: UserEntity = Depends(auth_user)):
    parameter_entity = await ParameterQuery().get_parameter_query(parameter_id)
    return parameter_entity.asdict()
