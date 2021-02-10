import 'moment/locale/fr';

import enUS from 'antd/lib/locale/en_US';
import frFR from 'antd/lib/locale/fr_FR';

import fr from '../locales/french.json';
import en from '../locales/english.json';

import { setCookie, getCookie } from '../lib/common.js';

const languages = { en, fr };
const locales = { en: enUS, fr: frFR };

window.i18n = (key) => window.i18nData[key];

window.changeLanguage = (lang) => {
  if (lang in languages) {
    window.i18nData = languages[lang];
    window.currentLanguage = lang;
    window.locale = locales[lang];
    setCookie('language', lang, {expires: 'Fri, 31 Dec 2100 23:59:59 GMT'});
  }
}

const getDefaultLanguage = () => {
  const defaultLang = getCookie('language') || window.navigator.language;
  let lang = defaultLang === 'fr' ? 'fr' : 'en';
  return lang;
}

window.changeLanguage(getDefaultLanguage());
