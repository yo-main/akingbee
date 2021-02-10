import { aristaeusApi } from '../../lib/common';

export async function createSwarm({health_status_id}) {
  let response = await aristaeusApi.post('/swarm', {health_status_id});
  return response.data;
}

export async function deleteSwarm({swarm_id}) {
  let response = await aristaeusApi.delete(`/swarm/${swarm_id}`);
  return response.data;
}