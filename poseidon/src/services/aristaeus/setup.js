import { aristaeusApi } from '../../lib/common';

export async function getSetupData(type) {
  let response = await aristaeusApi.get(`/setup/${type}`)
  return response.data;
}

export async function postSetupData(type, value) {
  let response = await aristaeusApi.post(`/setup/${type}`, {value});
  return response.data;
}

export async function updateSetupData(type, value, objectId) {
  let response = await aristaeusApi.put(`/setup/${type}/${objectId}`, {value});
  return response.data;
}

export async function deleteSetupData(type, objectId) {
  let response = await aristaeusApi.delete(`/setup/${type}/${objectId}`);
  return response.data;
}