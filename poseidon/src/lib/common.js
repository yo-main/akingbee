import { notification } from 'antd';
import axios from 'axios';

export function getCookie(name, cookies) {
  if (!cookies) {
    cookies = document.cookie;
  }
  cookies = document.cookie.split(";");
  cookies.forEach(cookie => {
    const data = cookie.split("=");
    if (data[0].trim() === name) {
      return data[1].trim();
    }
  })
  return null;
}

export function notificate(type, title, description) {
  notification[type]({
    message: title,
    description: description,
  });
}

axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*"
axios.defaults.headers.common["Content-Type"] = "application/json"

export const cerbesApi = axios.create({
  baseURL: 'http://127.0.0.1:9001'
})