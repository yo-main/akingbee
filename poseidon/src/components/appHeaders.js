import React from 'react';
import { Link, useHistory } from 'react-router-dom';
import { Menu, Row, Col } from 'antd';
import { HomeOutlined } from '@ant-design/icons';

import * as constants from '../constants';
import { logOff, getLoggerUserData } from '../services/authentication';

class LanguageMenu extends React.Component {
  render() {
    const items = Object.values(constants.languages).map((country) => (
      <Menu.Item key={country}>{country}</Menu.Item>
    ));

    return (
      <Menu theme="dark" mode="horizontal" defaultSelectedKeys={[window.currentLanguage]}>
        <Menu.SubMenu key="language_menu" title={window.i18n("word.language")} onClick={this.props.callback} id='language-menu'>
          {items}
        </Menu.SubMenu>
      </Menu>
    );
  }
}

export function LoggedOutMenu({ languageCallback }) {
  return (
    <Row justify="center">
      <Col span={12}>
        <Menu theme="dark" mode="horizontal" selectedKeys={[""]}>
          <Menu.Item><Link to={`/`}><HomeOutlined style={{fontSize: '17px'}} /></Link></Menu.Item>
        </Menu>
      </Col>
      <Col span={4} >
        <span style={{color: '#404040'}}>AKingBee {process.env.REACT_APP_VERSION}</span>
      </Col>
      <Col span={8}>
        <Row justify="end">
          <Col>
            <LanguageMenu callback={languageCallback} />
          </Col>
          <Col>
            <Menu theme="dark" mode="horizontal" selectedKeys={[]}>
              <Menu.Item><Link to={`/login`}>{window.i18n("word.login")}</Link></Menu.Item>
              <Menu.Item><Link to={`/register`}>{window.i18n("word.register")}</Link></Menu.Item>
            </Menu>
          </Col>
        </Row>
      </Col>
    </Row>
  )
}

export function LoggedInMenu({ languageCallback, section }) {
  let history = useHistory();

  let onClick = () => {
    logOff(history);
  }

  let username = getLoggerUserData("username")
  let is_admin= getLoggerUserData("admin") || getLoggerUserData("impersonator_id");

  let admin_menu = <></>;
  if (is_admin) {
    admin_menu = <Menu.Item key={constants.sections.menu_admin}><Link to={'/admin'}>{window.i18n("word.admin")}</Link></Menu.Item>
  }


  return (
    <Row justify="space-between">
      <Col>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={[section]}>
          <Menu.Item><Link to={`/`}><HomeOutlined style={{fontSize: '17px'}} /></Link></Menu.Item>
          <Menu.Item key={constants.sections.menu_manage}><Link to={`/manage`}>{window.i18n("word.manage")}</Link></Menu.Item>
          <Menu.Item key={constants.sections.menu_setup}><Link to={`/setup`}>{window.i18n("word.setup")}</Link></Menu.Item>
          <Menu.Item key={constants.sections.menu_profil}><Link to={`/profil`}>{window.i18n("word.profil")}</Link></Menu.Item>
          {admin_menu}
        </Menu>
      </Col>
      <Col>
          <span style={{color: '#404040'}}>AKingBee {process.env.REACT_APP_VERSION}</span>
      </Col>
      <Col>
        <Row>
          <Col>
            <span style={{color: 'white'}}>{window.i18n("word.welcome")} {username}</span>
          </Col>
          <Col>
            <LanguageMenu callback={languageCallback} />
          </Col>
          <Col>
            <Menu theme="dark" mode="horizontal">
              <Menu.Item onClick={onClick}>{window.i18n("word.logout")}</Menu.Item>
            </Menu>
          </Col>

        </Row>
      </Col>
    </Row>
  )
}

