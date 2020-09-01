import en from '../public/locales/english.json';
import fr from '../public/locales/french.json';
import { languages } from '../public/constants';
import { isLogged } from './auth';

export function getLocales(lang) {
  if (lang === 'fr') {
    return fr;
  }
  return en;
}

export function getLanguagePaths() {
  return Object.values(languages).map(
    (country) => ({ params: { lang: country } }),
  );
}

export function getFullPath(path) {
  const lang = window.location.pathname.split("/")[1];
  const url = "/" + lang + path;
  return url;
}

export function getBasicProps(params) {
  const locales = getLocales(params.lang);
  const lang = params.lang;
  const section = null;

  return {
    props: { locales, lang },
  };
}

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