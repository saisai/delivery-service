import {post, put} from "./api";

const OPERATOR_SHIFT_URL = '/api/operator/'

export async function endOperatorShift() {
  const token = localStorage.getItem('token');
  const userId = localStorage.getItem('user_id');
  return await put(`${OPERATOR_SHIFT_URL}${userId}/end/`, {
    "start_time": '2020-10-03'
  }, token)
}

export async function startOperatorShift() {
  const token = localStorage.getItem('token');
  const userId = localStorage.getItem('user_id');
  return await post(`${OPERATOR_SHIFT_URL}${userId}/start/`, {
    "start_time": '2020-10-04T18:38'
  }, token)
}