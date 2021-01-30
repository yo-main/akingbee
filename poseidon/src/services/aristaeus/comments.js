import { aristaeusApi } from '../../lib/common';
import { createSwarm } from './swarm';

export async function getCommentsByHive(hive_id) {
  let response = await aristaeusApi.get(`/comments/hive/${hive_id}`);
  return response.data;
}