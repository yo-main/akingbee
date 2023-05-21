import { notification } from 'antd';
import axios from 'axios';

import { UNLOGGED_STATUS, ERROR_STATUS, NOT_FOUND_STATUS } from '../pages/generic';

export function getCookie(name, cookies) {
  if (!cookies) {
    cookies = document.cookie;
  }
  cookies = document.cookie.split(";");
  let value = null;
  cookies.forEach((cookie) => {
    const data = cookie.split("=");
    if (data[0].trim() === name) {
      value = data[1].trim();
      return;
    }
  })
  return value;
}

export function setCookie(key, value, conf) {
  let cookie = `${key}=${value};`
  let cookieConf = {path: '/', samesite: 'lax', domain: window.location.hostname}
  Object.assign(cookieConf, conf)
  cookie += Object.keys(cookieConf).map((key) => {
    return [key, cookieConf[key]].join("=")
  }).join(";");
  document.cookie = cookie
}

export function notificate(type, description) {
  notification[type]({
    message: description,
  });
}

axios.defaults.headers.common["Content-Type"] = "application/json"

let cerbesUrl = `https://${process.env.REACT_APP_CERBES_SUB_DOMAIN}.${window.location.host}`
let aristaeusUrl = `https://${process.env.REACT_APP_ARISTAEUS_SUB_DOMAIN}.${window.location.host}`
if (process.env.NODE_ENV === "development") {
  cerbesUrl = `http://${process.env.REACT_APP_CERBES_SUB_DOMAIN}`;
  aristaeusUrl = `http://${process.env.REACT_APP_ARISTAEUS_SUB_DOMAIN}`;
}

export const cerbesApi = axios.create({
  baseURL: cerbesUrl,
  withCredentials: true,
})

export const aristaeusApi = axios.create({
  baseURL: aristaeusUrl,
  withCredentials: true,
})

export function dealWithError(error) {
  const response = error.response;

  if (!response) {
    notificate("error", error.message);
    return ERROR_STATUS;
  }

  if (response.status === 401 && window.location.pathname !== "/login") {
    return UNLOGGED_STATUS;
  }

  if (response.status === 404) {
    return NOT_FOUND_STATUS;
  }

  let msg;
  if (response.status === 422) {
    msg = response.data.detail.map(e => {
      return `${e.loc[1]}: ${e.msg}`
    }).join(", ")
  } else {
    let errorType = response.data.type;
    msg = window.i18n(`error.${errorType}`);
    if (!msg) {
      msg = response.data.message;
    }
  }

  notificate("error", msg)

  return ERROR_STATUS;
}