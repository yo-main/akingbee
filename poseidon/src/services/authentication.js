import { navigate } from '@reach/router';
import { getCookie, dealWithError } from '../lib/common';
import { AUTH_COOKIE_NAME } from '../constants';
import { cerbesApi, notificate, setCookie } from '../lib/common';

export function getJWT() {
  return getCookie(AUTH_COOKIE_NAME);
}

export function isLogged() {
  if (getJWT()) {
    return true;
  }
  return false;
}

export function storeJWT(jwt) {
  setCookie(AUTH_COOKIE_NAME, jwt);
}

export function clearJWT() {
  setCookie(AUTH_COOKIE_NAME, '', {'max-age': 0});
}

export function logOff() {
  clearJWT();
  navigate("/login")
}

export async function registrationRequest({email, username, password, password_bis}) {
  // checks
  if (password !== password_bis){
    notificate("error", window.i18n("error.passwordsNotIdentical"));
    return;
  }
  const language = window.currentLanguage;

  // request server to register user
  const data = {email, username, password, language}
  await cerbesApi.post("/user", data)
    .then((response) => {
      notificate("success", window.i18n("success.registrationSuccessful"));
      navigate("/login");
    })
    .catch((error) => {
      dealWithError(error);
    });
}

export async function loginRequest({username, password}) {
  const config = {
    auth: {username: username, password: password}
  };

  await cerbesApi.post("/login", null, config)
    .then((response) => {
      const token = response.data.access_token;
      storeJWT(token);
      notificate("success", window.i18n("success.loginSuccessful"));
      navigate("/");
    })
    .catch((error) => {
      dealWithError(error);
    });
}

export async function activationRequest({userId, activationId}) {
  let data = {user_id: userId, activation_id: activationId};
  let response = await cerbesApi.post('/activate', data);
  return response;
}

export async function resetPasswordRequest({username}) {
  let data = {username: username};
  let response = await cerbesApi.post('/password-reset/request', data);
  return response;
}

export async function validateResetId({userId, resetId}) {
  let data = {user_id: userId, reset_id: resetId};
  let response = await cerbesApi.get('/password-reset/validate', {params: data});
  return response;
}

export async function resetPassword({userId, resetId, password}) {
  let data = {user_id: userId, reset_id: resetId, password: password};
  let response = await cerbesApi.post('/password-reset', data)
  return response;
}