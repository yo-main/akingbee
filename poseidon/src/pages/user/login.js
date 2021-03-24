import React from 'react';
import { Link } from '@reach/router';
import { Form, Input, Button, Row, Space } from 'antd';

import { loginRequest } from '../../services/authentication';

export function LoginPage(props) {
  return (
    <Row justify="center" style={{ paddingTop: "150px"}}>
      <Form labelCol={{span: 8}} onFinish={loginRequest} requiredMark={false}>
        <Form.Item label={window.i18n('word.username')} name="username" rules={[{ required: true, message: window.i18n('form.insertUsernameMessage')}]}>
          <Input />
        </Form.Item>
        <Form.Item label={window.i18n('word.password')} name="password" rules={[{ required: true, message: window.i18n('form.insertPasswordMessage')}]}>
          <Input.Password />
        </Form.Item>
        <Form.Item wrapperCol={{offset: 8}}>
          <Space>
            <Button type="primary" htmlType="submit">
              {window.i18n('form.loginSubmit')}
            </Button>
            <Button>
              <Link to={`/password-reset`}>{window.i18n("action.passwordForgotten")}</Link>
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Row>
  )
}