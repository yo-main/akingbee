import { UnderlineOutlined } from '@ant-design/icons';
import { aristaeusApi, dealWithError, notificate } from '../../lib/common';

export async function getHives(callback) {
  await aristaeusApi.get(`/hive`)
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

export async function createHive({name, condition_id, owner_id, apiary_id, swarm_id, swarm_health_id}, callback) {
  if (swarm_id === undefined && swarm_health_id !== undefined) {
    let response = await aristaeusApi.post('/swarm', {health_status_id: swarm_health_id});
    swarm_id = response.data.id
  }

  let data = {name, condition_id, owner_id}

  if (apiary_id) {
    data.apiary_id = apiary_id;
  }
  if (swarm_id) {
    data.swarm_id = swarm_id;
  }

  console.log(data);

  await aristaeusApi.post(`/hive`, data)
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


export async function updateHive(hive_id, {name, owner_id, condition_id, swarm_id, apiary_id}, callback) {
  await aristaeusApi.put(`/hive/${hive_id}`, {name, owner_id, condition_id, swarm_id, apiary_id})
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


export async function deleteHive(hive_id, callback) {
  await aristaeusApi.delete(`/hive/${hive_id}`)
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