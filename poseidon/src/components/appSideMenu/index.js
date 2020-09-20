import React, { ReactComponent } from 'react';
import Icon from '@ant-design/icons';
import { Layout, Menu } from 'antd';

import { sections } from '../../constants';

import { ReactComponent as hiveIcon } from '../../images/beehouse.svg';
import { ReactComponent as apiaryIcon } from '../../images/location.svg';
import { ReactComponent as swarmIcon } from '../../images/bee.svg';

const { Sider } = Layout;
const { SubMenu } = Menu;

const hiveMenuIcon = <Icon component={hiveIcon} />;
const apiaryMenuIcon = <Icon component={apiaryIcon} />;
const swarmMenuIcon = <Icon component={swarmIcon} />;


export function ManageSideMenu(props) {
  return (
    <Sider className="site-layout-background" width={200}>
      <Menu
        mode="inline"
        defaultSelectedKeys={[sections.submenu_hive_list]}
        defaultOpenKeys={[sections.submenu_hive]}
        style={{ height: '100%' }}
      >
        <SubMenu key={sections.submenu_hive} icon={hiveMenuIcon} title={window.i18n("word.hives")}>
          <Menu.Item key={sections.submenu_hive_list}>{window.i18n("action.myHives")}</Menu.Item>
          <Menu.Item key={sections.submenu_hive_create}>{window.i18n("action.createHive")}</Menu.Item>
        </SubMenu>
        <SubMenu key={sections.submenu_apiary} icon={apiaryMenuIcon} title={window.i18n("word.apiaries")}>
          <Menu.Item key={sections.submenu_apiary_list}>{window.i18n("action.myApiaries")}</Menu.Item>
          <Menu.Item key={sections.submenu_apiary_create}>{window.i18n("action.createApiary")}</Menu.Item>
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
      >
        <SubMenu key={sections.submenu_setup_swarm} icon={swarmMenuIcon} title={window.i18n("action.setupSwarm")}>
          <Menu.Item key={sections.submenu_setup_swarm_health}>{window.i18n("word.health")}</Menu.Item>
        </SubMenu>
        <SubMenu key={sections.submenu_setup_hive} icon={hiveMenuIcon} title={window.i18n("action.setupHive")}>
          <Menu.Item key={sections.submenu_setup_hive_beekeeper}>{window.i18n("word.beekeeper")}</Menu.Item>
          <Menu.Item key={sections.submenu_setup_hive_condition}>{window.i18n("word.condition")}</Menu.Item>
          <Menu.Item key={sections.submenu_setup_hive_event}>{window.i18n("word.event")}</Menu.Item>
          <Menu.Item key={sections.submenu_setup_hive_honey_type}>{window.i18n("word.honeyType")}</Menu.Item>
        </SubMenu>
        <SubMenu key={sections.submenu_setup_apiary} icon={apiaryMenuIcon} title={window.i18n("action.setupApiary")}>
          <Menu.Item key={sections.submenu_setup_apiary_health}>{window.i18n("word.health")}</Menu.Item>
        </SubMenu>
      </Menu>
    </Sider>
  );
}