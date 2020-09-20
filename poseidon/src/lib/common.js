import { notification } from 'antd';
import axios from 'axios';

export function getCookie(name, cookies) {
  if (!cookies) {
    cookies = document.cookie;
  }
  cookies = document.cookie.split(";");
  let access_token = null;
  cookies.forEach((cookie) => {
    const data = cookie.split("=");
    if (data[0].trim() === name) {
      access_token = data[1].trim();
      return;
    }
  })
  return access_token;
}

export function notificate(type, description) {

  notification[type]({
    message: window.i18n(`word.${type}`),
    description: description,
  });
}

axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*"
axios.defaults.headers.common["Content-Type"] = "application/json"

export const cerbesApi = axios.create({
  baseURL: 'http://127.0.0.1:9001'
})


export function dealWithError(error) {
  const response = error.response;
  if (!response) {
    notificate("error", error.message);
  } else {
    notificate("error", response.data.detail)
  }
}