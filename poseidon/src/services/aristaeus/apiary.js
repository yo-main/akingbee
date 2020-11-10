import { aristaeusApi, dealWithError, notificate } from '../../lib/common';

export async function getApiaries(callback) {
  await aristaeusApi.get(`/apiary`)
    .then((response) => {
      const data = response.data;
      callback({data});
    })
    .catch((error) => {
      if (!error.response) {
        notificate("error", error.message);
      } else {
        dealWithError(error);
      }
    });
}

export async function createApiary({name, location, status, honey_type}, callback) {
  await aristaeusApi.post(`/apiary`, {name, location, status, honey_type})
    .then((response) => {
      callback();
    })
    .catch((error) => {
      if (!error.response) {
        notificate("error", error.message);
      } else {
        dealWithError(error);
      }
    });
}


export async function updateApiary(apiary_id, {name, location, status_id, honey_type_id}, callback) {
  await aristaeusApi.put(`/apiary/${apiary_id}`, {name, location, status_id, honey_type_id})
    .then((response) => {
      callback();
    })
    .catch((error) => {
      if (!error.response) {
        notificate("error", error.message);
      } else {
        dealWithError(error);
      }
    });
}


export async function deleteApiary(apiary_id, callback) {
  await aristaeusApi.delete(`/apiary/${apiary_id}`)
    .then((response) => {
      callback();
    })
    .catch((error) => {
      if (!error.response) {
        notificate("error", error.message);
      } else {
        dealWithError(error);
      }
    });
}