/* global i18n */
import fr from '../locales/french.json';
import en from '../locales/english.json';

const languages = { en, fr };

let defaultLanguage = window.navigator.language === 'fr' ? 'fr' : 'en';

window.i18nData = languages[defaultLanguage];
window.currentLanguage = defaultLanguage;

window.i18n = (key) => window.i18nData[key];

window.changeLanguage = (lang) => {
  if (lang in languages) {
    window.i18nData = languages[lang];
    window.currentLanguage = lang;
  }
}
