import {get} from "./api";


export async function getAllDataFromServer() {
  try {
    let data = {}
    const token = localStorage.getItem('token')
    data['cities'] = await get('/api/city/', token)
    data['districts'] = await get('/api/district/?city=1', token)
    data['streets'] = await get('/api/street/?city=1', token)
    return data
  } catch (e) {
    console.log(e)
  }
}

export async function fetchCouriersFromServer(date) {
  try {
    const token = localStorage.getItem('token');
    return await get(`/api/courier/?date=${date}`, token)
  } catch (e) {
    console.log(e)
  }
}

export async function fetchOrdersFromServer(date) {
  try {
    const token = localStorage.getItem('token');
    return await get(`/api/order/?date=${date}`, token)
  } catch (e) {
    console.log(e)
  }
}

export async function cityChangeDependencies(cityId) {
  try {
    const token = localStorage.getItem('token');
    data['districts'] = await get(`/api/district/?city=${cityId}`, token)
    data['streets'] = await get(`/api/street/?city=${cityId}`, token)
    return data
  } catch (e) {
    console.log(e)
  }

}

export async function districtChangeDependencies(districtId, cityId) {
  try {
    const token = localStorage.getItem('token');
    return await get(`/api/street/`, token)
  } catch (e) {
    console.log(e)
  }

}

export async function fetchAddressFromServer(address) {
  try {
    const token = localStorage.getItem('token');
    return await get(`/api/address/?custom_name=${address}`, token)
  } catch (e) {
    return e
  }
}

export async function checkOperatorShift(date) {
  const token = localStorage.getItem('token');
  const userId = localStorage.getItem('user_id');
  try {
    return await get(`/api/operator/check_shift/?date=${date}&user=${userId}`, token)
  } catch (e) {
    return e
  }
}