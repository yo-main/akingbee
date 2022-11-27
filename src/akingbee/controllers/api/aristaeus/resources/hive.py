import functools
from uuid import UUID

from akingbee.controllers.api.aristaeus.dtos.hive import HiveIn, HiveOut
from akingbee.controllers.api.aristaeus.utils.auth import auth_user
from akingbee.domains.aristaeus.applications.hive import HiveApplication
from akingbee.domains.aristaeus.commands.create_hive import CreateHiveCommand
from akingbee.domains.aristaeus.entities.hive import HiveEntity
from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.domains.aristaeus.queries.hive import HiveQuery
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("", response_model=HiveOut)
async def post_hive(input: HiveIn, user: UserEntity = Depends(auth_user)):
    command = CreateHiveCommand(
        name=input.name,
        condition=input.condition,
        owner_id=input.owner_id,
        apiary_id=input.apiary_id,
        organization_id=user.organization_id,
    )
    hive_application = HiveApplication()
    hive_entity = await hive_application.create(command=command)

    return hive_entity.asdict()


@router.get("/{hive_id}", response_model=HiveOut)
async def get_hive(hive_id: UUID, user: UserEntity = Depends(auth_user)):
    hive_entity = await HiveQuery().get_hive_query(hive_id)
    return hive_entity.asdict()
