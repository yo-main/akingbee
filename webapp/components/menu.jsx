import { Component } from 'react';
import { Layout, Menu, Row, Col } from 'antd';
import Link from 'next/link';
import Icon from '@ant-design/icons';
import * as constants from '../public/constants';
import { ids } from '../public/constants';
import hiveIcon from '../public/images/beehouse.svg';
import apiaryIcon from '../public/images/location.svg';
import swarmIcon from '../public/images/bee.svg';

const { SubMenu } = Menu;
const { Sider } = Layout;


class LanguageMenu extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current: props.current,
      locales: props.locales,
    };
  }

  changeLanguage({ key }) {
    let path = window.location.pathname.split("/");
    let base = window.location.origin;
    path[1] = key;

    let newUrl = `${base}${path.join("/")}`;

    window.location = newUrl;
  }

  render() {
    const items = Object.values(constants.languages).map((country) => (
      <Menu.Item key={country}>{country}</Menu.Item>
    ));

    return (
      <Menu theme="dark" mode="horizontal">
        <Menu.SubMenu key="language_menu" title={this.state.locales.Language} onClick={this.changeLanguage}>
          {items}
        </Menu.SubMenu>
      </Menu>
    );
  }
}

export function getMainMenu({locales, lang, hideMenu, section}) {
  if (hideMenu) {
    return (
      <Row gutter="10" justify="end">
        <Col>
          <Row>
            <Col>
              <LanguageMenu locales={locales} />
            </Col>
            <Col>
            <Menu theme="dark" mode="horizontal">
            <Menu.Item><Link href={`/${lang}/login`}><a>{locales.Login}</a></Link></Menu.Item>
            </Menu>
            </Col>
          </Row>
        </Col>
      </Row>
    );
  }

  return (
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
            <LanguageMenu locales={locales} />
          </Col>
          <Col>
          <Menu theme="dark" mode="horizontal">
          <Menu.Item>{locales.Logout}</Menu.Item>
          </Menu>
          </Col>
        </Row>
      </Col>
    </Row>
  );
}



export function getSideMenu({ section, locales }) {
  const hiveMenuIcon = <Icon component={hiveIcon} />;
  const apiaryMenuIcon = <Icon component={apiaryIcon} />;
  const swarmMenuIcon = <Icon component={swarmIcon} />;

  if (section === ids.section_manage) {
    return (
      <Sider className="site-layout-background" width={200}>
        <Menu
          mode="inline"
          defaultSelectedKeys={[ids.submenu_hive_list]}
          defaultOpenKeys={[ids.submenu_hive]}
          style={{ height: '100%' }}
        >
          <SubMenu key={ids.submenu_hive} icon={hiveMenuIcon} title={locales.Hives}>
            <Menu.Item key={ids.submenu_hive_list}>{locales.My_hives}</Menu.Item>
            <Menu.Item key={ids.submenu_hive_create}>{locales.Create_hive}</Menu.Item>
          </SubMenu>
          <SubMenu key={ids.submenu_apiary} icon={apiaryMenuIcon} title={locales.Apiaries}>
            <Menu.Item key={ids.submenu_apiary_list}>{locales.My_apiaries}</Menu.Item>
            <Menu.Item key={ids.submenu_apiary_create}>{locales.Create_apiary}</Menu.Item>
          </SubMenu>
        </Menu>
      </Sider>
    );
  }

  if (section === ids.section_setup) {
    return (
      <Sider className="site-layout-background" width={200}>
        <Menu
          mode="inline"
          style={{ height: '100%' }}
        >
          <SubMenu key={ids.submenu_setup_swarm} icon={swarmMenuIcon} title={locales.Setup_swarm}>
            <Menu.Item key={ids.submenu_setup_swarm_health}>{locales.Health}</Menu.Item>
          </SubMenu>
          <SubMenu key={ids.submenu_setup_hive} icon={hiveMenuIcon} title={locales.Setup_hive}>
            <Menu.Item key={ids.submenu_setup_hive_beekeeper}>{locales.Beekeeper}</Menu.Item>
            <Menu.Item key={ids.submenu_setup_hive_condition}>{locales.Condition}</Menu.Item>
            <Menu.Item key={ids.submenu_setup_hive_event}>{locales.Event}</Menu.Item>
            <Menu.Item key={ids.submenu_setup_hive_honey_type}>{locales.Honey_type}</Menu.Item>
          </SubMenu>
          <SubMenu key={ids.submenu_setup_apiary} icon={apiaryMenuIcon} title={locales.Setup_apiary}>
            <Menu.Item key={ids.submenu_setup_apiary_health}>{locales.Health}</Menu.Item>
          </SubMenu>
        </Menu>
      </Sider>
    );
  }

  return '';
}
