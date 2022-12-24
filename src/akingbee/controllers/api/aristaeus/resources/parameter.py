from uuid import UUID

from fastapi import APIRouter, Depends

from akingbee.controllers.api.aristaeus.dtos.parameter import (
    ParameterOut,
    PostParameterIn,
    PutParameterIn,
)
from akingbee.controllers.api.aristaeus.utils.auth import auth_user
from akingbee.domains.aristaeus.applications.parameter import ParameterApplication
from akingbee.domains.aristaeus.commands.parameter import (
    CreateParameterCommand,
    PutParameterCommand,
)
from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.domains.aristaeus.queries.parameter import ParameterQuery

router = APIRouter()


@router.post("", response_model=ParameterOut)
async def post_parameter(input: PostParameterIn, user: UserEntity = Depends(auth_user)):
    command = CreateParameterCommand(key=input.key, value=input.value, organization_id=user.organization_id)
    parameter_application = ParameterApplication()
    parameter_entity = await parameter_application.create(command=command)

    return parameter_entity.asdict()


@router.get("/{parameter_id}", response_model=ParameterOut)
async def get_parameter(parameter_id: UUID, user: UserEntity = Depends(auth_user)):
    parameter_entity = await ParameterQuery().get_parameter(parameter_id)
    return parameter_entity.asdict()


@router.get("", response_model=list[ParameterOut])
async def list_parameters(key: str | None = None, user: UserEntity = Depends(auth_user)):
    parameter_entities = await ParameterQuery().list_parameters(organization_id=user.organization_id, key=key)
    return [parameter.asdict() for parameter in parameter_entities]


@router.put("/{parameter_id}", response_model=ParameterOut)
async def put_parameter(parameter_id: UUID, input: PutParameterIn, user: UserEntity = Depends(auth_user)):
    command = PutParameterCommand(
        parameter_id=parameter_id,
        value=input.value,
    )
    parameter_application = ParameterApplication()
    parameter_entity = await parameter_application.put(command=command)
    return parameter_entity.asdict()


@router.delete("/{parameter_id}", status_code=204)
async def delete_parameter(parameter_id: UUID, user: UserEntity = Depends(auth_user)):
    parameter_application = ParameterApplication()
    await parameter_application.delete(public_id=parameter_id)
    return 204
