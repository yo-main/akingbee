import Frame from '../../components/layout';
import { getLocales, getLanguagePaths, getBasicProps } from '../../lib/common';
import { Body } from '../../components/body';

export default function Home({ locales, lang, loggedIn }) {
  const body = <Body />;
  return <Frame locales={locales} lang={lang} body={body} loggedIn={loggedIn} />;
}

export async function getStaticProps({ params }) {
  const props = getBasicProps(params);
  return props;
}

export async function getStaticPaths() {
  const paths = getLanguagePaths();
  return {
    paths,
    fallback: false,
  };
}
