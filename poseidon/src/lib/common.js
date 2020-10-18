import { notification } from 'antd';
import axios from 'axios';

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
  let cookieConf = {path: '/', samesite: 'strict'}
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

export const cerbesApi = axios.create({
  baseURL: 'http://localhost:9001',
  withCredentials: true,
})

export const aristaeusApi = axios.create({
  baseURL: 'http://localhost:9002',
  withCredentials: true,
})

export function dealWithError(error) {
  const response = error.response;
  if (!response) {
    notificate("error", error.message);
  } else {
    notificate("error", response.data.detail)
  }
}