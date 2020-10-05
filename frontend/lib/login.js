import {post, get} from "./api";

export async function loginPost(a, b) {
  try {
    const res = await post('/api/token-auth/',
      {
        "username": a,
        "password": b
      })
    return res
  } catch (e) {
    return e
  }
}

export async function whoAmI() {
  try {
    const token = localStorage.getItem('token')
    const res = await get('/api/user/me', token)
    return res
  } catch (e) {
    return e
  }
}