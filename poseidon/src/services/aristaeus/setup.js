import { aristaeusApi } from '../../lib/common';

export async function getSetupData(type) {
  let response = await aristaeusApi.get('/parameter', {params: {key: type}})
  return response.data;
}

export async function postSetupData(type, value) {
  let response = await aristaeusApi.post('/parameter', {params : {key: type, value: value}});
  return response.data;
}

export async function updateSetupData(type, value, objectId) {
  let response = await aristaeusApi.put(`/parameter/${objectId}`, {value});
  return response.data;
}

export async function deleteSetupData(type, objectId) {
  let response = await aristaeusApi.delete(`/parameter/${objectId}`);
  return response.data;
}