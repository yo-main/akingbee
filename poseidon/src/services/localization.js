/* global i18n */
import fr from '../locales/french.json';
import en from '../locales/english.json';

import { setCookie, getCookie } from '../lib/common.js';

const languages = { en, fr };

window.i18n = (key) => window.i18nData[key];

window.changeLanguage = (lang) => {
  if (lang in languages) {
    window.i18nData = languages[lang];
    window.currentLanguage = lang;
    setCookie('language', lang, {expires: 'Fri, 31 Dec 2100 23:59:59 GMT'});
  }
}

const getDefaultLanguage = () => {
  const lang = getCookie('language') || window.navigator.language;
  return (lang === 'fr' ? 'fr' : 'en');
}
window.changeLanguage(getDefaultLanguage());
