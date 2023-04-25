from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from aristaeus.controllers.api.dtos.swarm import PostSwarmIn
from aristaeus.controllers.api.dtos.swarm import PutSwarmIn
from aristaeus.controllers.api.dtos.swarm import SwarmOut
from aristaeus.controllers.api.utils.auth import auth_user
from aristaeus.domain.services.swarm import SwarmApplication
from aristaeus.domain.commands.swarm import CreateSwarmCommand
from aristaeus.domain.commands.swarm import PutSwarmCommand
from aristaeus.domain.entities.user import UserEntity
from aristaeus.domain.queries.swarm import SwarmQuery

router = APIRouter()


@router.post("", response_model=SwarmOut)
async def post_swarm(input: PostSwarmIn, user: UserEntity = Depends(auth_user)):
    command = CreateSwarmCommand(health_status=input.health, queen_year=input.queen_year)
    swarm_application = SwarmApplication()
    swarm_entity = await swarm_application.create_swarm(command=command)

    return swarm_entity.asdict()


@router.get("/{swarm_id}", response_model=SwarmOut)
async def get_swarm(swarm_id: UUID, user: UserEntity = Depends(auth_user)):
    swarm_entity = await SwarmQuery().get_swarm(swarm_id)
    return swarm_entity.asdict()


@router.put("/{swarm_id}", response_model=SwarmOut)
async def put_swarm(swarm_id: UUID, input: PutSwarmIn, user: UserEntity = Depends(auth_user)):
    command = PutSwarmCommand(swarm_id=swarm_id, health_status=input.health, queen_year=input.queen_year)
    swarm_application = SwarmApplication()
    swarm_entity = await swarm_application.put(command=command)
    return swarm_entity.asdict()


@router.delete("/{swarm_id}")
async def delete_swarm(swarm_id: UUID, user: UserEntity = Depends(auth_user)):
    swarm_application = SwarmApplication()
    await swarm_application.delete_swarm(swarm_id=swarm_id)
    return 204
