import { aristaeusApi } from '../../lib/common';
import { createSwarm } from './swarm';

export async function getCommentsForHive(hive_id) {
  let response = await aristaeusApi.get(`/comments/hive/${hive_id}`);
  return response.data;
}

export async function postCommentForHive(hive_id, {comment, date}) {
  let response = await aristaeusApi.post(`/comments/hive/${hive_id}`);
  return response.data;
}