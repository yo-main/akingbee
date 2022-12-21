from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from akingbee.controllers.api.aristaeus.dtos.hive import HiveOut, PostHiveIn, PutHiveIn
from akingbee.controllers.api.aristaeus.utils.auth import auth_user
from akingbee.domains.aristaeus.applications.hive import HiveApplication
from akingbee.domains.aristaeus.commands.hive import CreateHiveCommand, PutHiveCommand
from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.domains.aristaeus.queries.hive import HiveQuery

router = APIRouter()


@router.post("", response_model=HiveOut, status_code=201)
async def post_hive(input: PostHiveIn, user: UserEntity = Depends(auth_user)):
    command = CreateHiveCommand(
        name=input.name,
        condition=input.condition,
        owner_id=input.owner_id,
        apiary_id=input.apiary_id,
        swarm_id=input.swarm_id,
        organization_id=user.organization_id,
    )
    hive_application = HiveApplication()
    hive_entity = await hive_application.create(command=command)

    return hive_entity.asdict()


@router.get("", response_model=list[HiveOut])
async def list_hives(user: UserEntity = Depends(auth_user)):
    hive_entities = await HiveQuery().list_hives(organization_id=user.organization_id)
    return [hive.asdict() for hive in hive_entities]


@router.get("/{hive_id}", response_model=HiveOut)
async def get_hive(hive_id: UUID, user: UserEntity = Depends(auth_user)):
    hive_entity = await HiveQuery().get_hive_query(hive_id)
    return hive_entity.asdict()


@router.put("/{hive_id}", response_model=HiveOut)
async def put_hive(hive_id: UUID, input: PutHiveIn, user: UserEntity = Depends(auth_user)):
    command = PutHiveCommand(
        hive_id=hive_id, name=input.name, condition=input.condition, apiary_id=input.apiary_id, owner_id=input.owner_id
    )
    hive_application = HiveApplication()
    hive_entity = await hive_application.put(command=command)
    return hive_entity.asdict()


@router.delete("/{hive_id}", status_code=204)
async def delete_hive(hive_id: UUID, user: UserEntity = Depends(auth_user)):
    hive_application = HiveApplication()
    await hive_application.delete(hive_id=hive_id)
    return 204
