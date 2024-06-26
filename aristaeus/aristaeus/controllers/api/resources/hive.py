from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from aristaeus.controllers.api.dtos.hive import HarvestInput
from aristaeus.controllers.api.dtos.hive import HiveOut
from aristaeus.controllers.api.dtos.hive import PostHiveIn
from aristaeus.controllers.api.dtos.hive import PutHiveIn
from aristaeus.controllers.api.utils.auth import auth_user
from aristaeus.domain.commands.hive import CreateHiveCommand
from aristaeus.domain.commands.hive import HarvestCommand
from aristaeus.domain.commands.hive import MoveHiveCommand
from aristaeus.domain.commands.hive import PutHiveCommand
from aristaeus.domain.entities.user import User
from aristaeus.domain.queries.hive import HiveQuery
from aristaeus.domain.services.hive import HiveService

router = APIRouter()


@router.post("", response_model=HiveOut, status_code=201)
async def post_hive(input: PostHiveIn, user: User = Depends(auth_user)):
    command = CreateHiveCommand(
        name=input.name,
        condition=input.condition,
        owner=input.owner,
        apiary_id=input.apiary_id,
        swarm_id=input.swarm_id,
    )
    hive_service = HiveService()
    hive_entity = await hive_service.create(command=command, requester=user)

    return hive_entity.asdict()


@router.get("", response_model=list[HiveOut])
async def list_hives(with_apiary_only: bool | None = None, user: User = Depends(auth_user)):
    hive_entities = await HiveQuery().list_hives(
        organization_id=user.organization_id, with_apiary_only=with_apiary_only
    )
    return [hive.asdict() for hive in hive_entities]


@router.get("/{hive_id}", response_model=HiveOut)
async def get_hive(hive_id: UUID, user: User = Depends(auth_user)):
    hive_entity = await HiveQuery().get_hive_query(hive_id)
    return hive_entity.asdict()


@router.put("/{hive_id}", response_model=HiveOut)
async def put_hive(hive_id: UUID, input: PutHiveIn, user: User = Depends(auth_user)):
    command = PutHiveCommand(
        hive_id=hive_id, name=input.name, condition=input.condition, owner=input.owner, swarm_id=input.swarm_id
    )
    hive_service = HiveService()
    hive_entity = await hive_service.put(command=command, requester=user)
    return hive_entity.asdict()


@router.put("/{hive_id}/move/{apiary_id}", response_model=HiveOut)
async def move_hive(hive_id: UUID, apiary_id: UUID, user: User = Depends(auth_user)):
    command = MoveHiveCommand(hive_id=hive_id, apiary_id=apiary_id)
    hive_service = HiveService()
    hive = await hive_service.move_hive(command=command, requester=user)
    return hive.asdict()


@router.put("/{hive_id}/remove_apiary", response_model=HiveOut)
async def remove_apiary(hive_id: UUID, user: User = Depends(auth_user)):
    hive_service = HiveService()
    hive = await hive_service.remove_apiary(hive_id, requester=user)
    return hive.asdict()


@router.delete("/{hive_id}", status_code=204)
async def delete_hive(hive_id: UUID, user: User = Depends(auth_user)):
    hive_service = HiveService()
    await hive_service.delete(hive_id=hive_id)
    return 204


@router.post("/{hive_id}/harvest", status_code=204)
async def harvest_hive(hive_id: UUID, input: HarvestInput, user: User = Depends(auth_user)):
    hive_service = HiveService()
    command = HarvestCommand(
        hive_id=hive_id, quantity_in_grams=input.quantity_in_grams, date_harvest=input.date_harvest
    )
    await hive_service.harvest(hive_id, requester=user, command=command)
