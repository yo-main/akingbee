import React from 'react';
import Icon from '@ant-design/icons';
import { Layout, Menu } from 'antd';
import { Link } from '@reach/router';

import { sections } from '../constants';

import { ReactComponent as hiveIcon } from '../images/beehouse.svg';
import { ReactComponent as apiaryIcon } from '../images/location.svg';
import { ReactComponent as swarmIcon } from '../images/bee.svg';
import { ReactComponent as eventIcon } from '../images/events.svg';

const { Sider } = Layout;
const { SubMenu } = Menu;

const hiveMenuIcon = <Icon component={hiveIcon} />;
const apiaryMenuIcon = <Icon component={apiaryIcon} />;
const swarmMenuIcon = <Icon component={swarmIcon} />;
const eventMenuIcon = <Icon component={eventIcon} />;


export function ManageSideMenu(props) {

  return (
    <Sider className="site-layout-background" width={200}>
      <Menu
        mode="inline"
        defaultOpenKeys={[props.submenuTopic]}
        selectedKeys={[props.submenuItem]}
        style={{ height: '100%' }}
      >
        <SubMenu key={sections.submenu_hive} icon={hiveMenuIcon} title={window.i18n("word.hives")}>
          <Menu.Item key={sections.submenu_hive_list}><Link to='/manage/hive'>{window.i18n("action.myHives")}</Link></Menu.Item>
          <Menu.Item key={sections.submenu_hive_create}><Link to='/manage/hive/create'>{window.i18n("action.createHive")}</Link></Menu.Item>
        </SubMenu>
        <SubMenu key={sections.submenu_apiary} icon={apiaryMenuIcon} title={window.i18n("word.apiaries")}>
          <Menu.Item key={sections.submenu_apiary_list}><Link to='/manage/apiary'>{window.i18n("action.myApiaries")}</Link></Menu.Item>
          <Menu.Item key={sections.submenu_apiary_create}><Link to='/manage/apiary/create'>{window.i18n("action.createApiary")}</Link></Menu.Item>
        </SubMenu>
      </Menu>
    </Sider>
  );
}

export function SetupSideMenu(props) {
  return (
    <Sider className="site-layout-background" width={200}>
      <Menu
        mode="inline"
        style={{ height: '100%' }}
        defaultOpenKeys={[props.submenuTopic]}
        selectedKeys={[props.submenuItem]}
      >
        <SubMenu key={sections.submenu_setup_swarm} icon={swarmMenuIcon} title={window.i18n("action.setupSwarm")}>
          <Menu.Item key={sections.submenu_setup_swarm_health}><Link to='/setup/swarm/health'>{window.i18n("word.health")}</Link></Menu.Item>
        </SubMenu>
        <SubMenu key={sections.submenu_setup_hive} icon={hiveMenuIcon} title={window.i18n("action.setupHive")}>
          <Menu.Item key={sections.submenu_setup_hive_beekeeper}><Link to='/setup/hive/beekeeper'>{window.i18n("word.beekeepers")}</Link></Menu.Item>
          <Menu.Item key={sections.submenu_setup_hive_condition}><Link to='/setup/hive/condition'>{window.i18n("word.conditions")}</Link></Menu.Item>
        </SubMenu>
        <SubMenu key={sections.submenu_setup_apiary} icon={apiaryMenuIcon} title={window.i18n("action.setupApiary")}>
          <Menu.Item key={sections.submenu_setup_apiary_honey_type}><Link to='/setup/apiary/honey_type'>{window.i18n("word.honeyTypes")}</Link></Menu.Item>
        </SubMenu>
        <SubMenu key={sections.submenu_setup_event} icon={eventMenuIcon} title={window.i18n("action.setupEvent")}>
          <Menu.Item key={sections.submenu_setup_event_type}><Link to='/setup/event/type'>{window.i18n("word.types")}</Link></Menu.Item>
          <Menu.Item key={sections.submenu_setup_event_status}><Link to='/setup/event/status'>{window.i18n("word.status")}</Link></Menu.Item>
        </SubMenu>
      </Menu>
    </Sider>
  );
}