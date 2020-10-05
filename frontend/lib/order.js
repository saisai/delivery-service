import {post} from "./api";

const ORDER_URL = '/api/order/'

export async function makeOrder(data) {
  const token = localStorage.getItem('token')
  console.log(data)
  const payload = {
    courier_shift: data.courier,
    created_by: localStorage.getItem('user_id'),
    info: data.additionalInfo.comment,
    delivery_from: data.addressFrom,
    delivery_to: data.addressTo,
    ransom_sum: data.addressFrom.ransom_sum ? data.addressFrom.ransom_sum : 0,
    delivery_cost: data.addressTo.delivery_sum ? data.addressTo.delivery_sum : 0,
  }
  return await post(ORDER_URL, payload, token)
}