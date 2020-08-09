import Frame from '../../../components/layout';
import { getLocales, getLanguagePaths } from '../../../lib/common';
import * as constants from '../../../constants';

export default function Home({ locales, lang }) {
  return <Frame locales={locales} lang={lang} section={constants.ids.section_setup} />;
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
