import { aristaeusApi } from '../../lib/common';
import { createSwarm } from './swarm';

export async function getHives(withApiaryOnly) {
  let data = {with_apiary_only: withApiaryOnly};
  let response = await aristaeusApi.get(`/hive`, {params: data});
  return response.data;
}

export async function getHive(hiveId) {
  let response = await aristaeusApi.get(`/hive/${hiveId}`);
  return response.data;
}

export async function createHive({name, condition, owner, apiary_id, swarm_id, swarm_health}) {
  if (swarm_id === undefined && swarm_health !== undefined) {
    let swarm = await createSwarm({health: swarm_health, queen_year: new Date().getFullYear()});
    swarm_id = swarm.public_id;
  }

  let data = {name, condition, owner};

  if (apiary_id) {
    data.apiary_id = apiary_id;
  }

  if (swarm_id) {
    data.swarm_id = swarm_id;
  }

  let response = await aristaeusApi.post(`/hive`, data);
  return response.data;
}

export async function updateHive(hive_id, {name, owner, condition, swarm_id, apiary_id}) {
  let response = await aristaeusApi.put(`/hive/${hive_id}`, {name, owner, condition, swarm_id, apiary_id});
  return response.data;
}

export async function removeApiary(hiveId) {
  let response = await aristaeusApi.put(`/hive/${hiveId}/remove_apiary`);
  return response.data;
}

export async function deleteHive(hive_id) {
  let response = await aristaeusApi.delete(`/hive/${hive_id}`);
  return response.data;
}

export async function moveHive(hive_id, apiary_id) {
  let response = await aristaeusApi.put(`hive/${hive_id}/move/${apiary_id}`);
  return response.data;
}

export async function harvestHive(hive_id, {quantity_in_grams, date_harvest}) {
  let response = await aristaeusApi.post(`/hive/${hive_id}/harvest`, {quantity_in_grams, date_harvest});
  return response.data;
}
