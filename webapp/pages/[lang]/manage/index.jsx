import Frame from '../../../components/layout';
import * as constants from '../../../constants';
import { getLocales, getLanguagePaths } from '../../../lib/common';

export default function Home({ locales, lang }) {
  return <Frame locales={locales} section={constants.ids.section_manage} lang={lang} />;
}

export async function getStaticProps({ params }) {
  const { lang } = params;
  const locales = getLocales(lang);
  return {
    props: { locales, lang },
  };
}

export async function getStaticPaths() {
  const paths = getLanguagePaths();
  return {
    paths,
    fallback: false,
  };
}
