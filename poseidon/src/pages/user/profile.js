import React from 'react';
import { Row, Card } from 'antd';

import { getLoggerUserData } from '../../services/authentication';

export function ProfilePage(props) {
  return (
    <Row justify="left" style={{ paddingTop: "50px"}}>
      <Card title={window.i18n("title.userInformation")} type="inner">
        <p>{window.i18n('word.username')}: {getLoggerUserData('username')}</p>
        <p>{window.i18n('word.email')}: {getLoggerUserData('email')}</p>
      </Card>
    </Row>
  )
}