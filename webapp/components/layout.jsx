import Head from 'next/head';
import Link from 'next/link';
import { Layout, Menu, Breadcrumb, Row, Col, Dropdown, Button } from 'antd';
import getSideMenu from './sidemenu';
import * as constants from '../constants';

const { Header, Content, Footer } = Layout;


function changeLanguage({ item, key, keyPath, domEvent }) {
  let path = window.location.pathname.split("/");
  let base = window.location.origin;
  path[1] = key;

  let newUrl = `${base}${path.join("/")}`;

  window.location = newUrl;
}


function languageMenu(locales) {
  const items = Object.values(constants.languages).map((country) => (
    <Menu.Item key={country}>{country}</Menu.Item>
  ));

  return (
    <Menu theme="dark" mode="horizontal">
      <Menu.SubMenu key="language_menu" title={locales.Language} onClick={changeLanguage}>
        {items}
      </Menu.SubMenu>
    </Menu>
  );
}

export default function Frame({ lang, locales, section }) {
  const headData = (
    <Head>
      <title>aKingBee</title>
      <meta charSet="UTF-8" />
      <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      <meta name="description" content="A website dedicated to bees and beekeepers" />
      <link rel="icon" href="/favicon.ico" />
    </Head>
  );

  const mainMenu = (
    <Row gutter="10" justify="space-between">
      <Col>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={[section]}>
          <Menu.Item key={constants.ids.section_manage}><Link href={`/${lang}/manage`}><a>{locales.Manage}</a></Link></Menu.Item>
          <Menu.Item key={constants.ids.section_setup}><Link href={`/${lang}/setup`}><a>{locales.Setup}</a></Link></Menu.Item>
          <Menu.Item key={constants.ids.section_profil}><Link href={`/${lang}/profil`}><a>{locales.Profil}</a></Link></Menu.Item>
        </Menu>
      </Col>
      <Col>
        <Row>
          <Col>
            {languageMenu(locales)}
          </Col>
          <Col>
          <Menu theme="dark" mode="horizontal">
          <Menu.Item>Logout</Menu.Item>
          </Menu>
          </Col>
        </Row>
      </Col>
    </Row>
  );

  const headerData = (
    <Header className="header">
      <div className="logo" />
      {mainMenu}
    </Header>
  );

  const breadcrumbData = (
    <Breadcrumb style={{ margin: '16px 0' }}>
      <Breadcrumb.Item>Home</Breadcrumb.Item>
      <Breadcrumb.Item>List</Breadcrumb.Item>
      <Breadcrumb.Item>App</Breadcrumb.Item>
    </Breadcrumb>
  );

  const sideMenu = getSideMenu({ section, locales, lang });

  const footerData = (
    <Footer style={{ textAlign: 'center' }}>Ant Design ©2018 Created by Ant UED</Footer>
  );

  return (
    <Layout>
      {headData}
      {headerData}
      <Content style={{ padding: '0 50px' }}>
        <Layout className="site-layout-background" style={{ padding: '24px 0' }}>
          {sideMenu}
          <Content style={{ padding: '0 24px', minHeight: 280 }}>Content</Content>
        </Layout>
      </Content>
      {footerData}
    </Layout>
  );
}
