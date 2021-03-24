import React from 'react';

import { navigate } from '@reach/router';
import { Form, Input, Button, Row } from 'antd';
import { resetPasswordRequest, resetPassword, validateResetId } from '../../services/authentication';
import { LOADING_STATUS, getGenericPage, NOT_FOUND_STATUS } from '../generic';
import { dealWithError, notificate } from '../../lib/common';

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

  let passwordValidationRules = [
    {min: 8, message: window.i18n('form.heightCharactersMinimum')},
    {pattern: ".*[0-9]+.*", message: window.i18n('form.mustIncludeOneDigit')},
    {pattern: ".*[a-zA-Z]+.*", message: window.i18n('form.mustIncludeOneLetter')},
    {required: true, message: window.i18n('form.insertPasswordMessage')}
  ]

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

export function RequestPasswordResetPage(props) {
  let onSubmit = async({username}) => {
    try {
      await resetPasswordRequest({username})
    } catch (error) {}  // we don't want to show any particular error here

    notificate('success', window.i18n('sentence.processResetPassword'))
  }

  return (
    <Row justify="center" style={{ paddingTop: '150px'}}>
      <Form labelCol={{span: 8}} onFinish={onSubmit} requiredMark={false}>
        <Form.Item label={window.i18n('word.username')} name="username" rules={[{ required: true, message: window.i18n('form.insertUsernameMessage')}]}>
          <Input />
        </Form.Item>
        <Form.Item wrapperCol={{offset: 8}}>
          <Button type="primary" htmlType="submit">
            {window.i18n('confirm.resetPassword')}
          </Button>
        </Form.Item>
      </Form>
    </Row>
  )
}

export class PasswordResetPage extends React.Component {
  state = {pageStatus: LOADING_STATUS}

  async componentDidMount() {
    try {
      await validateResetId({userId: this.props.userId, resetId: this.props.resetId})
      this.setState((state) => {
        state["pageStatus"] = null;
        return state;
      })
    } catch (error) {
      this.setState((state) => {
        state["pageStatus"] = NOT_FOUND_STATUS;
        return state;
      })
    }
  }

  async onFinish(form) {
    try {
      await resetPassword(form);
      notificate("success", window.i18n("success.passwordReseted"));
      navigate("/login");
    } catch (error) {
      dealWithError(error);
    }
  }

  render() {
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };

    return (
      <Row justify="center" style={{ paddingTop: '150px'}}>
        <ResetPasswordForm userId={this.props.userId} resetId={this.props.resetId} onFinish={this.onFinish} />
      </Row>
    )
  }
}

