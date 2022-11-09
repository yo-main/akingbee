from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends

from akb.domains.bee.commands.create_swarm import CreateSwarmCommand
from akb.domains.bee.applications.swarm import SwarmApplication
from akb.domains.bee.queries.swarm import SwarmQuery
from akb.domains.bee.entities.swarm import SwarmEntity

from akb.controllers.api.bee.dtos.swarm import SwarmIn
from akb.controllers.api.bee.dtos.swarm import SwarmOut
from akb.controllers.api.bee.utils.auth import get_logged_in_user

router = APIRouter()


@router.post("/", response_model=SwarmOut)
async def post_swarm(self, input: SwarmIn, user: UUID = Depends(get_logged_in_user)):
    command = CreateSwarmCommand(health_status=input.health, queen_year=input.queen_year)
    swarm_application = SwarmApplication()
    swarm_entity = await swarm_application.create_async(command=command)
    return swarm_entity


@router.get("/{swarm_id}", response_model=SwarmOut)
async def get_swarm(self, swarm_id: UUID, user: UUID = Depends(get_logged_in_user)) -> SwarmEntity:
    return await SwarmQuery().get_swarm_query(swarm_id)
