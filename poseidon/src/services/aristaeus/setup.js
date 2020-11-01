import { navigate } from '@reach/router';
import { aristaeusApi, dealWithError, notificate } from '../../lib/common';

export function getData(type, callback) {
  aristaeusApi.get(`/setup/${type}`)
    .then((response) => {
      const data = response.data.reduce((acc, val, index) => {
        acc.push({
          key: index+1,
          id: val.id,
          name: val.name,
        });
        return acc;
      }, []);
      callback(data);
    })
    .catch((error) => {
      console.log(error)
      const response = error.response;
      if (!response) {
        notificate("error", error.message);
      } else if (error.response.status === 401) {
        navigate("/login");
      } else {
        dealWithError(error);
      }
    });
}

export async function postNewData(type, value, callback) {
  await aristaeusApi.post(`/setup/${type}`, {value})
    .then((response) => {
      callback();
    })
    .catch((error) => {
      console.log(error)
      const response = error.response;
      if (!response) {
        notificate("error", error.message);
      } else if (error.response.status === 401) {
        navigate("/login");
      } else {
        dealWithError(error);
      }
    });
}