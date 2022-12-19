/* eslint-disable require-jsdoc */
export async function request(url, method, body, headers) {
  return fetch(url, {
    mode: 'cors',
    method: method,
    headers: headers,
    body: (method === 'GET') ? null : JSON.stringify(body),
  }).then((response) => {
    return response;
  });
};
