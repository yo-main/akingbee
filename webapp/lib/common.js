import en from '../public/locales/english.json';
import fr from '../public/locales/french.json';
import { languages } from '../constants';

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
