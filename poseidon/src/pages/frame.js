import React from 'react';
import { Layout, Affix } from 'antd';
import { Redirect } from '@reach/router';

import { LoggedInMenu, LoggedOutMenu, ManageSideMenu, SetupSideMenu } from '../components';
import { isLogged } from '../services/authentication';

const { Header, Content } = Layout;


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
      <Layout style={{ 'min-height': '100vh' }}>
        <Affix offsetTop='0'>
          <Header className="header">
            <div className="logo" />
            <MainMenu section={section} languageCallback={this.props.languageCallback}/>
          </Header>
        </Affix>
        <Content style={{ padding: '0 50px'}}>
          <Layout className="site-layout-background" style={{ padding: '24px 0', 'min-height': '93vh'}}>
            <SideMenu submenuTopic={this.props.submenuTopic} submenuItem={this.props.submenuItem} />
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
  const logged = isLogged();
  return <Frame {...props} isLoggedIn={logged} />
}
