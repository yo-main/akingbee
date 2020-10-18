import React from 'react';
import { Layout } from 'antd';
import { Redirect } from '@reach/router';

import { LoggedInMenu, LoggedOutMenu, ManageSideMenu, SetupSideMenu } from '../components';
import { isLogged } from '../services/authentication';

const { Header, Content, Footer } = Layout;


class Frame extends React.Component {
  render() {

    const section = this.props.path.split("/")[1];

    const MainMenu = this.props.isLoggedIn ? LoggedInMenu : LoggedOutMenu;

    let SideMenu = () => "";

    if (section === "manage") {
      SideMenu = ManageSideMenu;
    } else if (section === "setup") {
      SideMenu = SetupSideMenu;
    }

    return (
      <Layout style={{ height: '100%' }}>
        <Header className="header">
            <div className="logo" />
            <MainMenu section={section} languageCallback={this.props.languageCallback}/>
        </Header>
        <Content style={{ padding: '0 50px' }}>
          <Layout className="site-layout-background" style={{ padding: '24px 0', height: '100vh' }}>
            <SideMenu />
            <Content>
              {this.props.children}
            </Content>
          </Layout>
        </Content>
      </Layout>
    )
  };
}

export function PrivateFrame(props) {
  const logged = isLogged();
  if (!logged) {
    return <Redirect to="/login" noThrow />
  }
  return <Frame {...props} isLoggedIn={true} />
}

export function PublicFrame(props) {
  return <Frame {...props} isLoggedIn={false} />
}
