import { aristaeusApi } from '../../lib/common';
import moment from 'moment';

export async function getCommentsForHive(hive_id) {
  let response = await aristaeusApi.get(`/comments/hive/${hive_id}`);
  let data = response.data;
  return data.reduce((acc, val) => {
    val['date'] = moment(val.date);
    acc.push(val);
    return acc;
  }, []);
}

export async function postCommentForHive(hive_id, { comment, date }) {
  let response = await aristaeusApi.post(`/comments/hive/${hive_id}`, { comment, date });
  return response.data;
}

export async function putComment(commentId, { comment, date }) {
  let response = await aristaeusApi.put(`/comments/${commentId}`, { comment, date });
  return response.data;
}

export async function deleteComment(commentId) {
  let response = await aristaeusApi.delete(`/comments/${commentId}`);
  return response.data;
}
