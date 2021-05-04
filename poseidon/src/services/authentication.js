import { navigate } from '@reach/router';
import { getCookie, dealWithError } from '../lib/common';
import { AUTH_COOKIE_NAME } from '../constants';
import { cerbesApi, notificate, setCookie } from '../lib/common';

export function getJWT() {
  return getCookie(AUTH_COOKIE_NAME);
}

export function isLogged() {
  let jwt = getJWT();
  if (!jwt) {
    return false;
  }

  let content = decodeJWT(jwt);
  let expiry_date = new Date(content.exp * 1000);
  return expiry_date > new Date();
}

function decodeJWT(jwt) {
  return JSON.parse(atob(jwt.split('.')[1]))
}

export function storeJWT(jwt) {
  let content = decodeJWT(jwt)
  let expiry_date = new Date(content.exp * 1000);
  setCookie(AUTH_COOKIE_NAME, jwt, {'expires': expiry_date.toUTCString()});
}

export function getLoggerUserData(key) {
  let content = decodeJWT(getJWT());
  return content[key];
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

async function logIn({username, password}) {
  const config = {
    auth: {username: username, password: password}
  };

  let response = await cerbesApi.post("/login", null, config)
  return response.data.access_token;
}

export async function loginRequest({username, password}) {
  try {
    let token = await logIn({username, password});
    storeJWT(token);
  } catch (error) {
    dealWithError(error);
    return;
  }

  notificate("success", window.i18n("success.loginSuccessful"));
  navigate("/");
  setTimeout(() => {loginRefresh({username, password})}, 5*1000*60);
}

async function loginRefresh({username, password}) {
  console.log("REFRESHING")

  if (!isLogged()) {
    return;
  };

  try {
    let token = await logIn({username, password});
    storeJWT(token);
  } catch (error) {
    console.log("Could not refresh JWT token");
    return;
  }

  setTimeout(() => {loginRefresh({username, password})}, 60*5*1000);
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