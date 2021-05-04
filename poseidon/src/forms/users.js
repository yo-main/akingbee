import React from 'react';

import { Form, Input, Button } from 'antd';

import { passwordValidationRules } from '../constants';

export function ResetPasswordForm(props) {
  const [form] = Form.useForm();

  form.setFieldsValue({
    "resetId": props.resetId,
    "userId": props.userId,
  })

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
    <Form labelCol={{span: 14, pull: 7}} form={form} wrapperCol={{pull: 7}} labelAlign='right' onFinish={props.onFinish} requiredMark={false}>
      <Form.Item label={window.i18n('word.newPassword')} name="password" rules={passwordValidationRules}>
        <Input.Password />
      </Form.Item>
      <Form.Item label={window.i18n('word.newPasswordBis')} name="passwordBis" rules={passwordValidationRulesBis}>
        <Input.Password />
      </Form.Item>
      <Form.Item name="resetId" hidden />
      <Form.Item name="userId" hidden />
      <Form.Item wrapperCol={{offset: 14, pull: 7}}>
      <Button type="primary" htmlType="submit">
        {window.i18n('confirm.resetPassword')}
      </Button>
      </Form.Item>
    </Form>
  )
}
