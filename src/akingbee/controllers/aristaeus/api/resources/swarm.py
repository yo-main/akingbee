from uuid import UUID

from fastapi import APIRouter, Depends

from akingbee.controllers.aristaeus.api.dtos.swarm import SwarmIn, SwarmOut
from akingbee.controllers.aristaeus.api.utils.auth import auth_user
from akingbee.domains.aristaeus.applications.swarm import SwarmApplication
from akingbee.domains.aristaeus.commands.create_swarm import CreateSwarmCommand
from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.domains.aristaeus.queries.swarm import SwarmQuery

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
