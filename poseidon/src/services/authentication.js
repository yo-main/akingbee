import { navigate } from '@reach/router';
import { getCookie, dealWithError } from '../lib/common';
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

export async function registrationRequest({email, username, password, password_bis}) {
  // checks
  if (password != password_bis){
    notificate("error", window.i18n("error.passwordsNotIdentical"))
    return;
  }

  // request server to register user
  const data = {email, username, password}
  await cerbesApi.post("/user", data)
    .then((response) => {
      notificate("success", window.i18n("success.registrationSuccessful"))
      navigate("/login")
    })
    .catch((error) => {
      dealWithError(error);
    });
}

export async function loginRequest({username, password}) {
  const data = {username, password}
  await cerbesApi.post("/login", data)
    .then((response) => {
      const token = response.data.access_token;
      storeJWT(token);
      notificate("success", window.i18n("success.loginSuccessful"))
      navigate("/")
    })
    .catch((error) => {
      dealWithError(error);
    });
}