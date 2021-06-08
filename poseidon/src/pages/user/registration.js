import React from 'react';
import { Form, Input, Button, Row } from 'antd';

import { registrationRequest } from '../../services/authentication';
import { passwordValidationRules } from '../../constants';

export function RegistrationPage(props) {
  const [form] = Form.useForm();

  let passwordValidator = (rule, value) => {
    if (value.length < 8) {
      return Promise.resolve();
    }
    if (form.getFieldValue("password") === form.getFieldValue("password_bis")) {
      return Promise.resolve();
    }
    return Promise.reject();
  }

  let passwordValidationRulesBis = [
    {required: true, message: window.i18n('form.insertPasswordMessage')},
    {validator: passwordValidator, message: window.i18n('form.passwordsMustBeSame')}
  ]

  let onFinish = (data) => {
    data['history'] = props.history;
    return registrationRequest(data);
  }

  return (
    <Row justify="center" style={{ paddingTop: "150px"}}>
      <Form labelCol={{span: 12, pull: 6}} wrapperCol={{pull: 6}} form={form} onFinish={onFinish} requiredMark={false}>
        <Form.Item label={window.i18n('word.username')} name="username" rules={[{ required: true, message: window.i18n('form.insertUsernameMessage')}]}>
          <Input />
        </Form.Item>
        <Form.Item label={window.i18n('word.email')} name="email" rules={[{type: 'email', message: window.i18n('form.mustBeAnEmail')}, {required: true, message: window.i18n('form.insertEmailMessage')}]}>
          <Input />
        </Form.Item>
        <Form.Item label={window.i18n('word.password')} name="password" rules={passwordValidationRules}>
          <Input.Password />
        </Form.Item>
        <Form.Item label={window.i18n('word.passwordBis')} name="password_bis" rules={passwordValidationRulesBis}>
          <Input.Password />
        </Form.Item>
        <Form.Item wrapperCol={{offset: 12, pull: 6}}>
          <Button type="primary" htmlType="submit">
            {window.i18n('word.submit')}
          </Button>
        </Form.Item>
      </Form>
    </Row>
  )
}