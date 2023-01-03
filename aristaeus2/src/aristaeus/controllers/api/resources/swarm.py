from uuid import UUID

from fastapi import APIRouter, Depends

from aristaeus.controllers.api.dtos.swarm import SwarmIn, SwarmOut
from aristaeus.controllers.api.utils.auth import auth_user
from aristaeus.domain.applications.swarm import SwarmApplication
from aristaeus.domain.commands.create_swarm import CreateSwarmCommand
from aristaeus.domain.entities.user import UserEntity
from aristaeus.domain.queries.swarm import SwarmQuery

router = APIRouter()


@router.post("", response_model=SwarmOut)
async def post_swarm(input: SwarmIn, user: UserEntity = Depends(auth_user)):
    command = CreateSwarmCommand(health_status=input.health, queen_year=input.queen_year)
    swarm_application = SwarmApplication()
    swarm_entity = await swarm_application.create_swarm(command=command)

    return swarm_entity.asdict()


@router.get("/{swarm_id}", response_model=SwarmOut)
async def get_swarm(swarm_id: UUID, user: UserEntity = Depends(auth_user)):
    swarm_entity = await SwarmQuery().get_swarm(swarm_id)
    return swarm_entity.asdict()
