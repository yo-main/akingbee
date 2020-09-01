import 'antd/dist/antd.css';
import Router from 'next/router';
import App from 'next/app';
import { isLogged, getJWT } from '../lib/auth';
import { getFullPath } from '../lib/common';
import { unstable_renderSubtreeIntoContainer } from 'react-dom';
import { AUTH_COOKIE_NAME } from '../public/constants';

// This default export is required in a new `pages/_app.js` file.
function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

MyApp.getInitialProps = async appContext => {
  const appProps = await App.getInitialProps(appContext);
  const ctx = appContext.ctx;

  if (ctx && ctx.req) {
    const lang = ctx.query.lang;
    const cookie = ctx.req.headers.cookie;
    if (lang && (!cookie || !cookie.includes(AUTH_COOKIE_NAME)) && !(ctx.pathname === "/[lang]/login")) {
      ctx.res.statusCode = 302;
      ctx.res.setHeader("Location", `/${lang}/login`);
    }
  } else {
    if (!isLogged()) {
      const url = getFullPath("/login");
      Router.push(url);
    }
  }
  return { ...appProps }
}

export default MyApp;