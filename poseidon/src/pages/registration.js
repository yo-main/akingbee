import React from 'react';
import { Form, Input, Button, Row } from 'antd';

import { registrationRequest } from '../services/authentication';

export function RegistrationPage(props) {
  return (
    <Row justify="center" style={{ paddingTop: "150px"}}>
      <Form labelCol={{span: 12}} onFinish={registrationRequest}>
        <Form.Item label={window.i18n('word.username')} name="username" rules={[{ required: true, message: window.i18n('form.insertUsernameMessage')}]}>
          <Input />
        </Form.Item>
        <Form.Item label={window.i18n('word.email')} name="email" rules={[{ required: true, message: window.i18n('form.insertEmailMessage')}]}>
          <Input />
        </Form.Item>
        <Form.Item label={window.i18n('word.password')} name="password" rules={[{ required: true, message: window.i18n('form.insertPasswordMessage')}]}>
          <Input.Password />
        </Form.Item>
        <Form.Item label={window.i18n('word.password_bis')} name="password_bis" rules={[{ required: true, message: window.i18n('form.insertPasswordMessage')}]}>
          <Input.Password />
        </Form.Item>
        <Form.Item wrapperCol={{offset: 12, span: 3}}>
          <Button type="primary" htmlType="submit">
            {window.i18n('form.loginSubmit')}
          </Button>
        </Form.Item>
      </Form>
    </Row>
  )
}