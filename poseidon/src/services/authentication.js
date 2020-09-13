import { getCookie } from '../lib/common';
import { AUTH_COOKIE_NAME } from '../constants';
import { cerbesApi, notificate } from '../lib/common';

export function getJWT() {
  return getCookie(AUTH_COOKIE_NAME);
}

export function isLogged() {
  if (getJWT()) {
    return true;
  }
  return false;
}

export function storeJWT({ jwt }) {
  document.cookie = `${AUTH_COOKIE_NAME}=${jwt};path='/';samesite`;
}

export function clearJWT() {
  document.cookie = `${AUTH_COOKIE_NAME}="";max-age=0`;
}

export async function loginRequest({email, username, password}) {
  const data = {email, username, password}
  await cerbesApi.post("/user", data)
    .then((response) => {
      console.log(response)
    })
    .catch((error) => {
      const response = error.response;
      const detail = response.data.detail;
      notificate("error", "Error", detail);
    });
}