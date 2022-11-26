from uuid import UUID
import functools
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from akingbee.domains.aristaeus.commands.create_swarm import CreateSwarmCommand
from akingbee.domains.aristaeus.applications.swarm import SwarmApplication
from akingbee.domains.aristaeus.queries.swarm import SwarmQuery
from akingbee.domains.aristaeus.entities.swarm import SwarmEntity

from akingbee.controllers.api.aristaeus.dtos.swarm import SwarmIn
from akingbee.controllers.api.aristaeus.dtos.swarm import SwarmOut
from akingbee.controllers.api.aristaeus.utils.auth import auth_user

router = APIRouter()


@router.post("", response_model=SwarmOut)
async def post_swarm(input: SwarmIn, user: UUID = Depends(auth_user)):
    command = CreateSwarmCommand(health_status=input.health, queen_year=input.queen_year)
    swarm_application = SwarmApplication()
    swarm_entity = await swarm_application.create_swarm(command=command)

    return swarm_entity.asdict()


@router.get("/{swarm_id}", response_model=SwarmOut)
async def get_swarm(swarm_id: UUID, user: UUID = Depends(auth_user)):
    swarm_entity = await SwarmQuery().get_swarm(swarm_id)
    return swarm_entity.asdict()
