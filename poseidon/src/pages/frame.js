import React from 'react';
import { Layout } from 'antd';
import { navigate } from '@reach/router';

import { MainMenu, SideMenu } from '../components';
import { isLogged } from '../services/authentication';

const { Header, Content, Footer } = Layout;


function frame(props, isLoggedIn) {
  return (
    <Layout style={{ height: '100%' }}>
      <Header className="header">
          <div className="logo" />
          <MainMenu path={props.path} languageCallback={props.languageCallback} isLoggedIn={isLoggedIn} />
      </Header>
      <Content style={{ padding: '0 50px' }}>
        <Layout className="site-layout-background" style={{ padding: '24px 0', height: '100vh' }}>
          <SideMenu path={props.path} />
          {props.children}
        </Layout>
      </Content>
    </Layout>
  );
}

export function PrivateFrame(props) {
  const logged = isLogged();
  if (!logged) {
    navigate('/login')
  }
  return frame(props, true)
}

export function PublicFrame(props) {
  return frame(props, false)
}
