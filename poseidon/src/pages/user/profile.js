import React from 'react';
import { Form, Input, Button, Row, Card } from 'antd';

import { getLoggerUserData } from '../../services/authentication';

import { ResetPasswordForm } from '../../forms/users';

export function ProfilePage(props) {
  const [form] = Form.useForm();

  let passwordValidator = (rule, value) => {
    if (value.length < 8) {
      return Promise.resolve();
    }
    if (form.getFieldValue("password") === form.getFieldValue("passwordBis")) {
      return Promise.resolve();
    }
    return Promise.reject();
  }

  let passwordValidationRulesBis = [
    {required: true, message: window.i18n('form.insertPasswordMessage')},
    {validator: passwordValidator, message: window.i18n('form.passwordsMustBeSame')}
  ]

  return (
    <Row justify="left" style={{ paddingTop: "50px"}}>
      <Card title={window.i18n("title.userInformation")} type="inner">
        <p>{window.i18n('word.username')}: {getLoggerUserData('username')}</p>
        <p>{window.i18n('word.email')}: {getLoggerUserData('email')}</p>
      </Card>
    </Row>
  )
}