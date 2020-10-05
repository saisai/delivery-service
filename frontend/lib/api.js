const GET = 'GET';
const POST = 'POST';
const PUT = 'PUT';
const PATCH = 'PATCH';
const DELETE = 'DELETE';


function parseJsonOrReturnPlain(payload) {
  try {
    return JSON.parse(payload);
  } catch (err) {
    return payload;
  }
}

function getFetchParams(method, payload, token) {
  const tokenHeaderPart = !!token ? { 'Authorization': `Token ${token}` } : {};
  const fetchParams = {
    method,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      ...tokenHeaderPart
    },
  };
  if (payload) {
    fetchParams.body = JSON.stringify(payload);
  }
  return fetchParams;
}

async function makeRequest(method, url, payload, token, stubData) {
  if (stubData) {
    await setTimeout(1000);
    if (stubData.isError) {
      throw stubData;
    } else {
      return stubData;
    }
  }

  const sendRequest = fetch.bind(undefined, "http://localhost:8000"+url, getFetchParams(method, payload, token));
  let response = await sendRequest();
  const body = await response.text();
  if (response.status >= 400) {
    throw parseJsonOrReturnPlain(body);
  } else {
    return parseJsonOrReturnPlain(body);
  }
}

export async function get(url, token, stubData) {
  return await makeRequest(GET, url, undefined, token, stubData);
}

export async function post(url, payload, token, stubData) {
  return await makeRequest(POST, url, payload, token, stubData);
}

export async function put(url, payload, token, stubData) {
  return await makeRequest(PUT, url, payload, token, stubData);
}

export async function patch(url, payload, token, stubData) {
  return await makeRequest(PATCH, url, payload, token, stubData);
}

export async function remove(url, token, stubData) {
  return await makeRequest(DELETE, url, undefined, token, stubData);
}