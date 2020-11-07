import React, { ReactComponent } from 'react';
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


const MANAGE_SECTIONS = {
  "/manage": [],
  "/manage/hive": [sections.submenu_hive, sections.submenu_hive_list],
  "/manage/hive/create": [sections.submenu_hive, sections.submenu_hive_create],
  "/manage/apiary": [sections.submenu_apiary, sections.submenu_apiary_list],
  "/manage/apiary/create": [sections.submenu_apiary, sections.submenu_apiary_create],
}

export function ManageSideMenu(props) {
  const url = window.location.pathname;
  const defaultSections = MANAGE_SECTIONS[url];

  return (
    <Sider className="site-layout-background" width={200}>
      <Menu
        mode="inline"
        defaultOpenKeys={[defaultSections[0]]}
        defaultSelectedKeys={[defaultSections[1]]}
        style={{ height: '100%' }}
      >
        <SubMenu key={sections.submenu_hive} icon={hiveMenuIcon} title={window.i18n("word.hives")}>
          <Menu.Item key={sections.submenu_hive_list}>{window.i18n("action.myHives")}</Menu.Item>
          <Menu.Item key={sections.submenu_hive_create}>{window.i18n("action.createHive")}</Menu.Item>
        </SubMenu>
        <SubMenu key={sections.submenu_apiary} icon={apiaryMenuIcon} title={window.i18n("word.apiaries")}>
          <Menu.Item key={sections.submenu_apiary_list}><Link to='/manage/apiary'>{window.i18n("action.myApiaries")}</Link></Menu.Item>
          <Menu.Item key={sections.submenu_apiary_create}><Link to='/manage/apiary/create'>{window.i18n("action.createApiary")}</Link></Menu.Item>
        </SubMenu>
      </Menu>
    </Sider>
  );
}

const SETUP_SECTIONS = {
  "/setup": [],
  "/setup/swarm/health": [sections.submenu_setup_swarm, sections.submenu_setup_swarm_health],
  "/setup/hive/beekeeper": [sections.submenu_setup_hive, sections.submenu_setup_hive_beekeeper],
  "/setup/hive/condition": [sections.submenu_setup_hive, sections.submenu_setup_hive_condition],
  "/setup/apiary/status": [sections.submenu_setup_apiary, sections.submenu_setup_apiary_status],
  "/setup/apiary/honey_type": [sections.submenu_setup_apiary, sections.submenu_setup_apiary_honey_type],
  "/setup/event/type": [sections.submenu_setup_event, sections.submenu_setup_event_type],
  "/setup/event/status": [sections.submenu_setup_event, sections.submenu_setup_event_status],
}

export function SetupSideMenu(props) {
  const url = window.location.pathname;
  const defaultSections = SETUP_SECTIONS[url];

  return (
    <Sider className="site-layout-background" width={200}>
      <Menu
        mode="inline"
        style={{ height: '100%' }}
        defaultOpenKeys={[defaultSections[0]]}
        defaultSelectedKeys={[defaultSections[1]]}
      >
        <SubMenu key={sections.submenu_setup_swarm} icon={swarmMenuIcon} title={window.i18n("action.setupSwarm")}>
          <Menu.Item key={sections.submenu_setup_swarm_health}><Link to='/setup/swarm/health'>{window.i18n("word.health")}</Link></Menu.Item>
        </SubMenu>
        <SubMenu key={sections.submenu_setup_hive} icon={hiveMenuIcon} title={window.i18n("action.setupHive")}>
          <Menu.Item key={sections.submenu_setup_hive_beekeeper}><Link to='/setup/hive/beekeeper'>{window.i18n("word.beekeepers")}</Link></Menu.Item>
          <Menu.Item key={sections.submenu_setup_hive_condition}><Link to='/setup/hive/condition'>{window.i18n("word.conditions")}</Link></Menu.Item>
        </SubMenu>
        <SubMenu key={sections.submenu_setup_apiary} icon={apiaryMenuIcon} title={window.i18n("action.setupApiary")}>
          <Menu.Item key={sections.submenu_setup_apiary_status}><Link to='/setup/apiary/status'>{window.i18n("word.status")}</Link></Menu.Item>
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