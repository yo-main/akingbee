import { aristaeusApi } from '../../lib/common';

export async function getApiaries() {
  let response = await aristaeusApi.get(`/apiary`)
  return response.data;
}

export async function createApiary({name, location, honey_type}) {
  let response = await aristaeusApi.post(`/apiary`, {name, location, honey_type});
  return response.data;
}


export async function updateApiary(apiary_id, {name, location, honey_type_id}) {
  let response = await aristaeusApi.put(`/apiary/${apiary_id}`, {name, location, honey_type_id});
  return response.data;
}


export async function deleteApiary(apiary_id) {
  let response = await aristaeusApi.delete(`/apiary/${apiary_id}`);
  return response.data;
}