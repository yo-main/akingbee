import { aristaeusApi } from '../../lib/common';

export async function createSwarm({health, queen_year}) {
  let response = await aristaeusApi.post('/swarm', {health, queen_year});
  return response.data;
}

export async function updateSwarm(swarmId, {health, queen_year}) {
  let response = await aristaeusApi.put(`/swarm/${swarmId}`, {health, queen_year});
  return response.data;
}

export async function deleteSwarm({swarm_id}) {
  await aristaeusApi.delete(`/swarm/${swarm_id}`);
}