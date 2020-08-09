import { Layout, Menu } from 'antd';
import Icon from '@ant-design/icons';
import { ids } from '../constants';
import hiveIcon from '../public/images/beehouse.svg';
import apiaryIcon from '../public/images/location.svg';
import swarmIcon from '../public/images/bee.svg';

const { SubMenu } = Menu;
const { Sider } = Layout;



export default function getSideMenu({ section, locales, lang }) {
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
