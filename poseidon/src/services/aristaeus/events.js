import { aristaeusApi } from '../../lib/common';
import moment from 'moment';

export async function getEvents(hive_id) {
  let response = await aristaeusApi.get(`/event?hive_id=${hive_id}`);
  let data = response.data;
  return data.reduce((acc, val) => {
    val['due_date'] = moment(val.due_date);
    acc.push(val);
    return acc;
  }, []);
}

export async function postEvent({ title, description, dueDate, typeId, statusId, hiveId }) {
  let response = await aristaeusApi.post(`/event`, { hive_id: hiveId, title: title, description: description, due_date: dueDate, type_id: typeId, status_id: statusId });
  return response.data;
}

export async function putEvent(eventId, { title, description, dueDate, statusId }) {
  let response = await aristaeusApi.put(`/event/${eventId}`, { title: title, description: description, due_date: dueDate, status_id: statusId });
  return response.data;
}

export async function deleteEvent(eventId) {
  let response = await aristaeusApi.delete(`/event/${eventId}`);
  return response.data;
}
