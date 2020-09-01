import { getCookie } from '../lib/common';
import { AUTH_COOKIE_NAME } from '../public/constants';

export function getJWT(cookies) {
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
