import Frame from '../../components/layout';
import { getLocales, getLanguagePaths } from '../../lib/common';

export default function Home({ locales }) {
  return <Frame locales={locales} />;
}

export async function getStaticProps({ params }) {
  const locales = getLocales(params.lang);
  const section = null;

  return {
    props: { locales },
  };
}

export async function getStaticPaths() {
  const paths = getLanguagePaths();
  return {
    paths,
    fallback: false,
  };
}
